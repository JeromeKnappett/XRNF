#! /opt/local/bin/python
# PyNX - Python tools for Nano-structures Crystallography
#   (c) 2016-present : ESRF-European Synchrotron Radiation Facility
#       authors:
#         Vincent Favre-Nicolin, favre@esrf.fr
#   (C) 2020-2024 - Synchrotron SOLEIL
#       authors:
#         Nicolas Mille, nicolas.mille@synchrotron-soleil.fr
#         Picca Frederic-Emmanuel , picca@synchrotron-soleil.fr

import argparse
import functools
import os
import time

from dataclasses import dataclass
from fnmatch import fnmatch
from pathlib import Path
from typing import Dict, List, Optional, Union

import numexpr as ne

import numpy as np

from h5py import File, Dataset
from PIL import Image

from .runner import PtychoRunner, PtychoRunnerScan, PtychoRunnerException, \
    default_params as params0
from ...utils import phase

helptext_epilog = " Example:\n" \
                  "     pynx-ptycho-hermes --folder path/to/my/data/ --maxsize 1300 --threshold 10 " \
                  " --algorithm=AP**150,nbprobe=1,probe=1 --probediam 61e-9)\n\n" \
                  " The distance (SI units - in meters) between the " \
                  "detector and the sample can be guessed thanks to " \
                  "the annulus size.\n"\
                  " A calibration file is here :\n" \
                  "     /home/experiences/hermes/com-hermes/DATA/Sample2detector_Calculator.ods"

# The beamline specific default parameters
params_beamline = {
    # specific
    'adaptq': 'soft',
    'camcenter': None,
    'dark_as_optim': False,
    'logfile': "log_reconstruction_"
               f"{time.gmtime().tm_mon:.2f}_{time.gmtime().tm_year}.txt",
    'onlynrj': None,
    'encoder_coordinates': False,
    'ruchepath': None,
    'savefolder': None,
    'savellk': False,
    'savetiff': 'full',
    'threshold': 30,
}

params_generic_overwrite = {
    # overwrite generic parameters
    'algorithm': 'AP**150,nbprobe=1,probe=1',
    'detector_orientation': "1,0,0",
    'instrument': 'Hermes@Soleil',
    'maxsize': 1000,
    'obj_inertia': 0.1,
    'pixelsize': 11e-6,
    'probe': 'disc,61e-9',
    'probe_inertia': 0.01,
    'saveplot': True,
}

default_params = params0.copy()
default_params.update(params_beamline)
default_params.update(params_generic_overwrite)

H5PATH_ENERGY = '/entry1/camera/energy'
H5PATH_REAL_SAMPLE_X = '/entry1/camera/real_sample_x'
H5PATH_REAL_SAMPLE_Y = '/entry1/camera/real_sample_y'
H5PATH_SAMPLE_X = '/entry1/camera/sample_x'
H5PATH_SAMPLE_Y = '/entry1/camera/sample_y'
H5PATH_SSD_DISTANCE = '/entry1/scanArgs/SDDistance'

#############
# Dark File #
#############


@dataclass
class DarkFile:
    path: Path
    date: str
    num: int


def parse_dark_file(path: Path) -> Optional[DarkFile]:
    res = None
    fname = path.name
    if fnmatch(fname, "Image*_dark_000001.nxs") or fnmatch(fname, "image*_dark_000001.nxs") or fnmatch(fname, "Stack*_dark_000001.nxs") or fnmatch(fname, "stack*_dark_000001.nxs"):
        try:
            (_, date, num, _, _) = fname.split('_')
            res = DarkFile(path, date, int(num))
        except ValueError:
            pass
    return res


####################
# Description File #
####################

@dataclass
class DescrFile_Image:
    path: Path
    date: str
    num: int


@dataclass
class DescrFile_Stack:
    path: Path
    date: str
    num: int


DescrFile = Union[DescrFile_Image, DescrFile_Stack]


def parse_descr_file(path: Path) -> Optional[DescrFile]:
    res = None
    fname = path.name
    if fnmatch(fname, "Image*.hdf5"):
        (fn, _) = os.path.splitext(fname)
        try:
            (_, date, num) = fn.split('_')
            res = DescrFile_Image(path, date, int(num))
        except ValueError:
            pass
    elif fnmatch(fname, "Stack*.hdf5"):
        (fn, _) = os.path.splitext(fname)
        try:
            (_, date, num) = fn.split('_')
            res = DescrFile_Stack(path, date, int(num))
        except ValueError:
            pass
    return res

##############
# Image File #
##############


@dataclass
class DataFile_Image:
    path: Path
    date: str
    num: int


@dataclass
class DataFile_Stack:
    path: Path
    date: str
    num: int
    nrj: int


DataFile = Union[DataFile_Image, DataFile_Stack]


def parse_data_file(path: Path) -> Optional[DataFile]:
    res = None
    fname = path.name
    if (fnmatch(fname, "Stack*_000001.nxs") or fnmatch(fname, "stack*_000001.nxs")) and not (fnmatch(fname, "Stack*_dark_000001.nxs") or fnmatch(fname, "stack*_dark_000001.nxs")):
        try:
            (_, date, num, nrj, _) = fname.split('_')
            res = DataFile_Stack(path, date, int(num), int(nrj.replace('nrj', '')))
        except ValueError:
            pass
    elif (fnmatch(fname, "Image*_000001.nxs") or fnmatch(fname, "image*_000001.nxs")) and not (fnmatch(fname, "Image*_dark_000001.nxs") or fnmatch(fname, "image*_dark_000001.nxs")):
        try:
            (_, date, num, _) = fname.split('_')
            res = DataFile_Image(path, date, int(num))
        except ValueError:
            pass
    return res


############
# ScanType #
############


@dataclass
class ScanType_Image:
    descr: DescrFile_Image
    dark: DarkFile
    data: DataFile_Image


@dataclass
class ScanType_Stack:
    descr: DescrFile_Stack
    dark: DarkFile
    datas: Dict[int, DataFile_Stack]


ScanType = Union[ScanType_Image, ScanType_Stack]

#############
# ScanTypes #
#############


@dataclass
class ScanTypes_Images:
    images: Dict[int, ScanType_Image]


@dataclass
class ScanTypes_Stack:
    stack: ScanType_Stack


ScanTypes = Union[ScanTypes_Images, ScanTypes_Stack]


def get_ScanTypes(folder: Path,
                  scanids: Optional[Union[List[int]]] = None,
                  onlynrj: Optional[List[int]] = None) -> ScanTypes:
    # TODO add verbose

    scantypes: Optional[ScanTypes] = None
    _scantypes: Optional[Dict[int, ScanType]] = {}

    datafiles: Dict[int, List[DataFile]] = {}
    descrfiles: Dict[int, DescrFile] = {}
    darkfiles: Dict[int, DarkFile] = {}

    if folder.is_dir():
        for p in folder.iterdir():
            d = parse_descr_file(p)
            if d is not None:
                descrfiles[d.num] = d
                continue
            d = parse_data_file(p)
            if d is not None:
                if d.num in datafiles:
                    datafiles[d.num].append(d)
                else:
                    datafiles[d.num] = [d]
                continue
            d = parse_dark_file(p)
            if d is not None:
                darkfiles[d.num] = d
                continue

        for k, v in descrfiles.items():
            if k in darkfiles and k in datafiles:
                descr = v
                dark = darkfiles[k]
                datas = datafiles[k]
                if isinstance(v, DescrFile_Image):
                    if len(datas) == 1:
                        data = datas[0]
                        if isinstance(data, DataFile_Image):
                            _scantypes[k] = ScanType_Image(descr, dark, data)

                elif isinstance(v, DescrFile_Stack):
                    if len(datas) >= 1:
                        if all([isinstance(p, DataFile_Stack) for p in datas]):
                            _scantypes[k] = ScanType_Stack(descr, dark, {d.nrj: d for d in datas})

        print(f"Found {len(_scantypes)} experiments in the folder: {folder}")
        for k, v in _scantypes.items():
            print(f"-  {k}: {type(v)}")

        # filter scans with the users ids list
        if scanids is not None:
            _scantypes = {k:v for k, v in _scantypes.items() if k in scanids}
        print(f"Remaining {len(_scantypes)} experiments after filtering on scanids: {scanids}")
        for k, v in _scantypes.items():
            print(f"-  {k}: {type(v)}")

        # filter nrjs
        if onlynrj is not None:
            for k, v in _scantypes.items():
                if isinstance(v, ScanType_Stack):
                    v.datas = {v.nrj: v for v in datas if v.nrj in onlynrj}
            print(f"Remaining {len(_scantypes)} experiments after filtering with onlynrj: {onlynrj}")
            for k, v in _scantypes.items():
                print(f"-  {k}: {type(v)}")

        if not _scantypes:
            raise PtychoRunnerException(
                f"No scan found in folder: {folder}\n"
                "It could be because one of the file"
                " (data.nxs, dark.nxs or descr.hdf5) is missing")

        # check if this is list of images or one stack we deals with
        # only these two kind of experiments

        if all([isinstance(v, ScanType_Image) for k, v in _scantypes.items()]):
            scantypes = ScanTypes_Images(_scantypes)
        elif len(_scantypes) == 1:
            v = next(iter(_scantypes.values()))
            if isinstance(v, ScanType_Stack):
                scantypes = ScanTypes_Stack(v)

        if not scantypes:
            raise PtychoRunnerException(
                "It is not possible to process multiple Stack or a mix of Stack and Images")

    return scantypes


def scantypes_dark_filename_get(scantypes: ScanTypes, scan: int) -> Path:
    """get the descrfile from the scan index"""
    if isinstance(scantypes, ScanTypes_Images):
        return scantypes.images[scan].dark.path
    elif isinstance(scantypes, ScanTypes_Stack):
        return scantypes.stack.dark.path


def scantypes_description_filename_get(scantypes: ScanTypes, scan: int) -> Path:
    """get the descrfile from the scan index"""
    if isinstance(scantypes, ScanTypes_Images):
        return scantypes.images[scan].descr.path
    elif isinstance(scantypes, ScanTypes_Stack):
        return scantypes.stack.descr.path


def scantypes_image_filename_get(scantypes: ScanTypes, scan: int) -> Path:
    """get the descrfile from the scan index"""
    if isinstance(scantypes, ScanTypes_Images):
        return scantypes.images[scan].data.path
    elif isinstance(scantypes, ScanTypes_Stack):
        return scantypes.stack.datas[scan].path


def scantypes_saveprefix_get(scantypes: ScanTypes, scan: int, savefolder: Optional[Path]=None) -> Path:
    if isinstance(scantypes, ScanTypes_Images):
        image = scantypes.images[scan]
        tmpl = Path(f"image_{image.descr.date}" + r"_{scan:03d}_reconstructed_run{run:02d}")
    elif isinstance(scantypes, ScanTypes_Stack):
        image = scantypes.stack.datas[scan]
        prefix = f"stack_{image.date}_{scantypes.stack.descr.num:03d}"
        tmpl = Path(prefix + '_reconstructed') / Path(prefix + r"_nrj{scan:03d}_run{run:02d}")

    return Path(savefolder or image.data.path.parent) / Path('reconstructed') / tmpl


#########
# Utils #
#########

def wavelength(energy):
    """Compute the wavelength from the nrj.

    :param energy: X-ray energy in eV
    :return: wavelength in Angstroems
    """
    return 1239.84 * 1e-9 / energy


def calc_roi(start_roi, length, start_energy, this_energy):
    """Function to calculate the new ROI.

    in order to adapt Q space the software way
    """
    cam_pixel_size = 11.6 * 1e-6  # camera pixel size in µm TODO use
    # the params for this
    roi1 = cam_pixel_size * start_roi / 2
    theta1 = np.arctan(roi1 / length) * 180 / np.pi
    ll1 = wavelength(start_energy)
    ll2 = wavelength(this_energy)
    return round(length * np.tan(np.arcsin((ll2 / ll1) * np.sin(theta1 * np.pi / 180)))
                 * 1e+6 / 11.6 * 2)


def get_raw_data_dset(h5: File) -> Dataset:
    # data are saved under /<first entry>/scan_data/<fist dataset>
    first_entry_name = list(h5.keys())[0]
    sample_data_entry = h5.get(f"/{first_entry_name}/scan_data/")
    sample_data_imgname = list(sample_data_entry.keys())[0]
    # Loading only the images corresponding to the imgn variable
    # (in order to take into account moduloframe and maxframe
    # params) and broadcasting to float32.
    # Purpose of separating into two case is to avoid making a
    # copy if the full data are used (a copy is mandatory for the
    # sliced data, so it will be longer to load sliced data than
    # the full ones ... )
    return sample_data_entry.get(sample_data_imgname)

##########################
# PtychoRunnerScanHermes #
##########################

class PtychoRunnerScanHermesBase(PtychoRunnerScan):
    """Deal with Hermes Scans."""

    def __init__(self,
                 # specific parameters of PtychoRunnerScanHermesBase
                 scantypes: ScanTypes,
                 # default params of PtychoRunnerScan
                 params, scan, mpi_comm=None, timings=None):
        super().__init__(params, scan, mpi_comm, timings)
        self.scantypes = scantypes

    def load_scan(self):
        """Supersed of load_scan function from runner.

        Update x, y positions of the camera images as well as the
        number of images imgn

        When the scan type is an energy stack:
        ---> self.scan refer to the nrj number
             (from 01 to NN, NN being the total number of energies)
        When the scan type are separated files:
        ---> self.scan refer to the scan number XX,
             given by the Image_YYYYMMDD_XX.hdf5 file
        """
        if self.params['verbose']:
            if isinstance(self.scantypes, ScanTypes_Images):
                print(f'\nProcessing the image \n  - {self.scantypes.images[self.scan]}')
            elif isinstance(self.scantypes, ScanTypes_Stack):
                print(f'\nProcessing the stack {self.scan} which contains {len(self.scantypes.stack.datas)} nrj(s) {self.params["scan"]}\n')

        h5n = scantypes_description_filename_get(self.scantypes, self.scan)

        x = y = imgn = None

        with File(h5n, 'r') as h5:
            if self.params["encoder_coordinates"]:
                dset_x = h5[H5PATH_REAL_SAMPLE_X]
                dset_y = h5[H5PATH_REAL_SAMPLE_Y]
                if isinstance(self.scantypes, ScanTypes_Images):
                    x = np.ravel(dset_x.astype(np.float32)[()])
                    y = np.ravel(dset_y.astype(np.float32)[()])
                elif isinstance(self.scantypes,  ScanTypes_Stack):
                    x = np.ravel(dset_x.astype(np.float32)[self.scan - 1])
                    y = np.ravel(dset_y.astype(np.float32)[self.scan - 1])
            else:
                dset_x = h5[H5PATH_SAMPLE_X]
                dset_y = h5[H5PATH_SAMPLE_Y]
                n_x = len(dset_x)
                n_y = len(dset_y)

                x = np.empty(n_x * n_y, dtype=np.float32)
                x_tmp = np.empty(n_x, dtype=np.float32)
                dset_x.read_direct(x_tmp)

                y = np.empty(n_x * n_y, dtype=np.float32)
                y_tmp = np.empty(n_y, dtype=np.float32)
                dset_y.read_direct(y_tmp)

                # Here two options for the scan direction : switch True/False
                if True:
                    # Option 1 : The scan is in the type Y stays
                    # constant, scan X, step Y, rescan X, etc.
                    for j in range(n_y):
                        for i in range(n_x):
                            x[i + j * n_x] = x_tmp[i]
                            y[i + j * n_x] = y_tmp[j]
                else:
                    # Option 2 : The scan is in the type X stay
                    # constant, scan Y, step X, rescan Y, etc.
                    for i in range(n_x):
                        for j in range(n_y):
                            x[j + i * n_y] = x_tmp[i]
                            y[j + i * n_y] = y_tmp[j]

        # set values in meter
        x *= 1e-6
        y *= 1e-6

        # Imgn variable
        imgn = np.arange(len(x), dtype=int)

        if self.params['moduloframe'] is not None:
            n1, n2 = self.params['moduloframe']
            idx = np.where(imgn % n1 == n2)[0]

            x = x.take(idx)
            y = y.take(idx)
            imgn = imgn.take(idx)

        if self.params['maxframe'] is not None:
            maxframe = self.params['maxframe']
            if len(imgn) > maxframe:
                if self.params['verbose']:
                    print(f'MAXFRAME: only using first {maxframe} frames')

                x = x[:maxframe]
                y = y[:maxframe]
                imgn = imgn[:maxframe]

        self.x = x
        self.y = y
        self.imgn = imgn

    def load_data(self):
        """
        Supersed of load_data function from runner
        Update the raw_data variable with all the images

        Also update the energy variable here

        When the type of scan is energy stack:
        ---> self.scan refer to the nrj number
             (from 01 to NN, NN being the total number of energies)
        When the type of scan is separate files:
        ---> self.scan refer to the scan number XX,
             given by the Image_YYYYMMDD_XX.hdf5 file
        """

        # compute all filenames.
        h5n_dark = scantypes_dark_filename_get(self.scantypes, self.scan)
        h5n_sample = scantypes_image_filename_get(self.scantypes, self.scan)

        saveprefix = scantypes_saveprefix_get(self.scantypes, self.scan,
                                              self.params['savefolder'])
        self.params['saveprefix'] = str(saveprefix)

        # read all images
        start = time.time()
        with File(h5n_sample, 'r') as h5_sample:
            raw_data = None
            raw_data_dset = get_raw_data_dset(h5_sample)
            if self.imgn.shape[0] == raw_data_dset.shape[0]:
                raw_data = np.array(raw_data_dset, dtype=np.float32, copy=False)
            else:
                raw_data = np.array(raw_data_dset[self.imgn, :, :], dtype=np.float32, copy=False)
            self.raw_data = raw_data
        print(f"Loading data in {time.time() - start} seconds")


        # ead the dark and apply the correction
        with File(h5n_dark, 'r') as h5_dark:
            dark_data_dset = get_raw_data_dset(h5_dark)
            # Avoiding the first dark image (a generally not good one)
            dark_data = dark_data_dset[1:, :, :]
            dark_average = np.mean(dark_data, axis=0, dtype=np.float32)

            if self.params["dark_as_optim"] is False:
                print("dark subtraction and applying threshold")
                # Subtract dark and apply threshold: parallel with numexpr version
                ne_expression = "where(data - dark > thr, data - dark, 0)"
                ne_localdict = {"data": self.raw_data,
                                "dark": dark_average,
                                "thr": self.params["threshold"]}
                ne.evaluate(ne_expression, local_dict=ne_localdict, out=self.raw_data)

                # Bring dark_subtract to 0 in order not to subtract twice
                self.params["dark_subtract"] = 0

            else:
                # Load the dark in order to use it in the reconstruction
                print("dark loading...")
                self.dark = dark_average
                self.params["dark_subtract"] = 1

                if np.any(self.raw_data < 0):
                    raise PtychoRunnerException("some raw data below zero ??!!")


    def set_roi(self) -> None:
        # Check if a camera center has been given, and define the
        # according camera roi in that case
        camcenter = self.params['camcenter']
        maxsize = self.params['maxsize']
        if camcenter is not None:
            xmin = camcenter[0] - maxsize // 2
            xmax = camcenter[0] + maxsize // 2
            ymin = camcenter[1] - maxsize // 2
            ymax = camcenter[1] + maxsize // 2
            self.params['roi'] = f"{xmin},{xmax},{ymin},{ymax}"


    def save(self, run, stepnum=None, algostring=None):
        """Overwriting of the save function

        Purpose:
        - updating the reconstruction log file
        - saving llk value if user params says so

        The original function is called via super()
        Only a part is added at the end

        Save the result of the optimization, and (if
        self.params['saveplot'] is True) the corresponding plot.

        This is an internal function.

        :param run:  the run number (integer)
        :param stepnum: the step number in the set of algorithm steps
        :param algostring: the string corresponding to all the algorithms ran
        :return:
        """
        super().save(run, stepnum, algostring)
        self.update_logfile(run)

        # Save LLKs values in dedicated text file
        if self.params['savellk']:
            self.save_llk(run)

    def save_plot(self, run, stepnum=None, algostring=None,
                  display_plot=False):
        """
        Overwriting of the save_plot function

        Purpose: saving also the reconstruction data as four tif files:
        - two for the object (amplitude and phase)
        - two for the probe (amplitude and phase)

        The original function is called via super()
        Only a part is added at the end to do the tif files

        Save the plot to a png file.

        :param run:  the run number (integer)
        :param stepnum: the step number in the set of algorithm steps
        :param algostring: the string corresponding to all the algorithms ran
        :param display_plot: if True, the saved plot will also be displayed
        :return:
        """
        super().save_plot(run, stepnum, algostring, display_plot)

        if self.params["savetiff"] not in [None, "No"]:
            # Get the obj, probe and scanned area for the probe and
            # object (copy-pasted from parent function)
            if 'split' in self.params['mpi']:
                self.p.stitch(sync=True)
                obj = self.p.mpi_obj
                scan_area_obj = self.p.get_mpi_scan_area_obj()
                if not self.mpi_master:
                    return
            else:
                obj = self.p.get_obj()
                scan_area_obj = self.p.get_scan_area_obj()
            scan_area_probe = self.p.get_scan_area_probe()

            if (self.p.data.near_field or not self.params['remove_obj_phase_ramp']):
                obj = obj[0]
                probe = self.p.get_probe()[0]
            else:
                obj = phase.minimize_grad_phase(obj[0],
                                                center_phase=0,
                                                global_min=False,
                                                mask=~scan_area_obj,
                                                rebin_f=2)[0]
                probe = phase.minimize_grad_phase(self.p.get_probe()[0],
                                                  center_phase=0,
                                                  global_min=False,
                                                  mask=~scan_area_probe,
                                                  rebin_f=2)[0]

            # Get the amplitude and the phase of object
            if self.params["savetiff"] == "full":
                obj_amp = Image.fromarray(np.abs(obj))
                obj_phase = Image.fromarray(np.angle(obj))
                probe_amp = Image.fromarray(np.abs(probe))
                probe_phase = Image.fromarray(np.angle(probe))
            elif self.params["savetiff"] == "crop":
                # Get the indices of the object and probe where they
                # are actually reconstructed
                xmin_obj, ymin_obj = np.argwhere(scan_area_obj).min(axis=0)
                xmax_obj, ymax_obj = np.argwhere(scan_area_obj).max(axis=0)
                xmin_probe, ymin_probe = \
                    np.argwhere(scan_area_probe).min(axis=0)
                xmax_probe, ymax_probe = \
                    np.argwhere(scan_area_probe).max(axis=0)

                # This part is needed because sometimes (why ???),
                # scan_area_obj and scan_area_probe give a strange
                # size of the object (especially a non square
                # reconstructed image araise from a square scan ...)

                # object AMPLITUDE as Image cropped with the right size
                obj_amp = Image.fromarray(
                    np.abs(obj[xmin_obj:xmax_obj,
                               ymin_obj:ymax_obj]))
                # Object PHASE as Image cropped with the right size
                obj_phase = Image.fromarray(
                    np.angle(obj[xmin_obj:xmax_obj,
                                 ymin_obj:ymax_obj]))
                # Probe AMPLITUDE as Image cropped with the right size
                probe_amp = Image.fromarray(
                    np.abs(probe[xmin_probe:xmax_probe,
                                 ymin_probe:ymax_probe]))
                # Probe PHASE as Image cropped with the right size
                probe_phase = Image.fromarray(
                    np.angle(probe[xmin_probe:xmax_probe,
                                   ymin_probe:ymax_probe]))

            # Save the images
            prefix = self.get_scan_prefix(run, self.scan)
            obj_amp.save(prefix + '_Object_Amplitude.tif')
            obj_phase.save(prefix + '_Object_Phase.tif')
            probe_amp.save(prefix + '_Probe_Amplitude.tif')
            probe_phase.save(prefix + '_Probe_Phase.tif')

    def update_logfile(self, run):
        """Logfile updating function"""
        with open(self.params['logfile'], mode='a') as logfile:
            content = ["############################################\n"]
            content.append("date of reconstruction: " + time.asctime() + "\n")
            content.append("file reconstructed: "
                           + str(scantypes_image_filename_get(self.scantypes, self.scan))
                           + "\n")
            content.append("Run number: " + str(run) + "\n")

            for key, value in self.params.items():
                if key in ['algorithm', 'maxsize', 'threshold',
                           'detectordistance', 'rebin', 'defocus',
                           'probe']:
                    content.append(str(key) + " = " + str(value) + "\n")

            content.append(f"LLK={self.p.llk_poisson / self.p.nb_obs:.3f}\n")

            savepath = self.get_scan_prefix(run, self.scan)
            content.append("Saved in: " + savepath + ".cxi\n")
            content.append("END\n\n")

            logfile.writelines(content)
            if self.params['verbose']:
                print()
                print('Updated log file: ' + self.params['logfile'])
                print()

    def save_llk(self, run):
        """Save into a file the llk parameters"""
        all_llk = np.array([[k]
                            for k, v in self.p.history['llk_poisson'].items()])
        headerllk = "cycle\t"
        for whichllk in ['llk_poisson', 'llk_gaussian', 'llk_euclidian']:
            headerllk += whichllk + '\t'
            thisllk = np.array([[v]
                                for k, v in self.p.history[whichllk].items()])
            all_llk = np.concatenate((all_llk, thisllk), axis=1)
        llkfilename = self.get_scan_prefix(run, self.scan) \
                      + '_everyllk.txt'
        if self.params['verbose']:
            print("\nSaving all llk values in " + llkfilename + "\n")
        np.savetxt(llkfilename, all_llk, delimiter='\t', header=headerllk)


class PtychoRunnerScanHermesImages(PtychoRunnerScanHermesBase):
    """Deal with Hermes Scans."""

    def load_data(self):
        """
        Supersed of load_data function from runner
        Update the raw_data variable with all the images

        Also update the energy variable here

        When the type of scan is energy stack:
        ---> self.scan refer to the nrj number
             (from 01 to NN, NN being the total number of energies)
        When the type of scan is separate files:
        ---> self.scan refer to the scan number XX,
             given by the Image_YYYYMMDD_XX.hdf5 file
        """

        # load image and dark
        super().load_data()

        h5n = scantypes_description_filename_get(self.scantypes, self.scan)

        # load nrj
        with File(h5n, 'r') as hd5_scaninfo:
            nrj_dset = hd5_scaninfo.get(H5PATH_ENERGY)
            nrj = nrj_dset[()]
            nrjstart = 0  # useless for images
            print(f"Start loading data for image  number {self.scan} ;"
                  f" energy = {nrj} eV")

            self.params['nrj'] = nrj * 1e-3
            self.params['startnrj'] = nrjstart * 1e-3

        # set the roi and postprocess
        self.set_roi()
        self.load_data_post_process()


class PtychoRunnerScanHermesStack(PtychoRunnerScanHermesBase):
    """Deal with Hermes Scans."""

    def load_data(self):
        """
        Supersed of load_data function from runner
        Update the raw_data variable with all the images

        Also update the energy variable here

        When the type of scan is energy stack:
        ---> self.scan refer to the nrj number
             (from 01 to NN, NN being the total number of energies)
        When the type of scan is separate files:
        ---> self.scan refer to the scan number XX,
             given by the Image_YYYYMMDD_XX.hdf5 file
        """

        # read images and dark
        super().load_data()

        # compute all filenames.
        h5n = scantypes_description_filename_get(self.scantypes, self.scan)

        # load nrj and distance
        with File(h5n, 'r') as hd5_scaninfo:
            nrj_dset = hd5_scaninfo.get(H5PATH_ENERGY)
            nrj = nrj_dset[self.scan - 1]
            nrjstart = nrj_dset[0]
            print(f"Start loading data for nrj number {self.scan} ;"
                  f" energy0 = {nrjstart} eV"
                  f" energy  = {nrj} eV")

            self.params['nrj'] = nrj * 1e-3
            self.params['startnrj'] = nrjstart * 1e-3

            # Adapt the maxsize or the detector distance if it is an
            # energy stack depending if detector distance has been moved
            # (hard way: the detector distance changes) or not (software
            # way: maxsize changes)
            if self.scan != self.params["scan"][0]:
                if self.params["adaptq"] == 'soft':
                    self.params["maxsize"] = calc_roi(self.params["maxsizeini"],
                                                      self.params["detectordistance"],
                                                      self.params["startnrj"] * 1e3,
                                                      self.params["nrj"] * 1e3)
                elif self.params["adaptq"] == 'hard':
                    try:
                        self.params["detectordistance"] = \
                            hd5_scaninfo.get(H5PATH_SSD_DISTANCE)[self.scan - 1] * 1e-6
                    except Exception:  # TODO use the right exception
                        print("You wanted to use hard adaptq but the updated sample-detector distances \
                        are not found in the hdf5 descriptor file, reconstruction will continue \
                        without any q adaptation")

        self.set_roi()
        self.load_data_post_process()

######################
# PtychoRunnerHermes #
######################

def partialClass(cls, *args, **kwds):
    class NewCls(cls):
        __init__ = functools.partialmethod(cls.__init__, *args, **kwds)

    return NewCls


class PtychoRunnerHermes(PtychoRunner):
    """Class to process Hermes scans."""

    def __init__(self, argv, params, *args, **kwargs):
        super().__init__(argv, default_params if params is None else params)
        scantypes = get_ScanTypes(Path(self.params['folder']),
                                  self.params['scan'],
                                  self.params['onlynrj'])

        runner = None
        if isinstance(scantypes, ScanTypes_Images):
            runner = partialClass(PtychoRunnerScanHermesImages, scantypes)
        elif isinstance(scantypes, ScanTypes_Stack):
            # need to override the scan params and use the nrjs instead of the scan number
            # pynx use this list to iterate and set the self.scan value.
            self.params['scan'] = sorted([k for k in scantypes.stack.datas])
            runner = partialClass(PtychoRunnerScanHermesStack, scantypes)
        self.PtychoRunnerScan = runner

    @classmethod
    def make_parser(cls, default_par, description=None, script_name="pynx-ptycho-hermes", epilog=None):
        if epilog is None:
            epilog = helptext_epilog
        if description is None:
            description = "Script to perform a ptychography analysis on data from Hermes@Soleil"
        p = default_par

        parser = super().make_parser(default_par, script_name, description, epilog)
        grp = parser.add_argument_group("Hermes parameters")

        class ActionFolder(argparse.Action):
            """Argparse Action to check the folder exists"""

            def __call__(self, parser_, namespace, value, option_string=None):
                if not os.path.isdir(value):
                    raise argparse.ArgumentError(
                        self, f"--folder {value}: folder does not exist or is not a directory")
                setattr(namespace, self.dest, value)

        grp.add_argument('--folder', type=str, required=True, action=ActionFolder,
                         help="The path where the data are located (data.nxs, dark.nxs, "
                              "descr.hdf5 must all be there !)")

        grp.add_argument(
            '--threshold', type=int, default=p['threshold'],
            help='threshold, for the high pass filter. It correspond to the thermal '
                 'noise of the camera, after dark subtraction.')

        class ActionCamCenter(argparse.Action):
            """Argparse Action to check the folder exists"""

            def __call__(self, parser_, namespace, value, option_string=None):
                mes = f"--camcenter {' '.join(value)}: need two integers for " \
                      f"the the camera centre position, e.g. '--camcenter 1002 1036"
                try:
                    if len(value) == 1 and ',' in value[0]:
                        # Probably --camcenter=200,400
                        v = [int(s) for s in value[0].split(',')]
                    elif len(value) == 2:
                        v = [int(s) for s in value]
                    else:
                        raise argparse.ArgumentError(self, mes)
                except ValueError:
                    raise argparse.ArgumentError(self, mes)

                setattr(namespace, self.dest, v)

        grp.add_argument(
            '--camcenter', default=p['camcenter'], nargs='+',
            action=ActionCamCenter,
            help='The center of the camera, if the auto finding of PyNX do not '
                 'find the proper center of diffraction You should respect the '
                 'convention ``--camcenter x0 y0`` with x0 and y0 INTEGERS: the '
                 'coordinates x and y of the center in pixel coordinates. Do not '
                 'call this parameter to let PyNX find the center of diffraction.')

        grp.add_argument('--adaptq', type=str, default=p['adaptq'],
                         help="the way to adapt q:\n"
                              "Only used for energy stack (so if type=stack).\n"
                              "Defines the way to adapt the data to have a constant q space "
                              "in the reconstructions of the whole stack.\n"
                              "Takes only three values:\n\n"
                              "* 'soft': adapt the q space changing the 'maxsize' PyNX parameter. "
                              "  ⚠️ do it if you didn't make detector distance to move "
                              "during the stack\n"
                              "* 'hard': ⛔ NOT IMPLEMENTED YET ⛔. "
                              "adapt the q space changing the 'detector distance' parameter "
                              "according to the control program way to move it "
                              "⚠️ do it if you actually did make detector distance to move "
                              " during the stack\n"
                              "* ``none``: do not adaptq. "
                              "⚠️ do it only if you don't want to adapt q space\n\n"
                              "The default is ``soft``: it changes automatically the 'maxsize' parameter "
                              "taking into account the starting energy and the detector distance "
                              "to get the same q range and thus the same nbr of pixel in all the "
                              "reconstruction of the stack")

        # VFN: would be easier to use directly '--probe disc,60e-6' instead
        # of introducing a new 'probediam' parameter
        class ActionProbeDiam(argparse.Action):
            """Argparse Action to convert the 'probediam' entry to a string for 'probe' """

            def __call__(self, parser_, namespace, value, option_string=None):
                diam = float(value)
                setattr(namespace, self.dest, f"disc,{diam}")

        grp.add_argument(
            '--probediam', '--probe', dest='probe', action=ActionProbeDiam, required=True,
            help="Diameter of the probe in meters, at the focus "
                 "(it is 1.22 x FZP outerZone width).\n"
                 "⚠️ don't take into account the defocus here ⚠️")

        grp.add_argument(
            '--onlynrj', type=int, default=None, nargs='+',
            help="nrj numbers (indices in the stack) you want to reconstruct within a stack."
                 "If you want the whole stack, don't use this parameter.")

        # VFN: I'm not fond of this argument - it's simply the opposite of the
        # default argument "--dark_subtract". Also, I don't think subtracting the
        # background by default is a good idea. Though in this case the process is
        # different due to the 'filter' used with a threshold.
        grp.add_argument(
            '--dark_as_optim', action='store_true',
            help="Call this flag to use the dark as background for reconstruction "
                 "instead of subtracting it to each diffraction patter before the "
                 "reconstruction.\n\n"
                 "⚠️⚠️ If you use this, you may need to optimise the background"
                 " in your algorithm (background=1) ⚠️⚠️")

        grp.add_argument(
            '--ruchepath', type=str, default=None,
            help="e.g. /nfs/ruche-hermes/hermes-soleil/com-hermes/PTYCHO/some/path:\n"
                 "Path where only the Amplitude.tif will be saved. Useful to have "
                 "directly access to it for XMCD on another computer")

        # VFN: TODO: Not implemented. Have a look at --save_prefix which is quite flexible and
        #            should probably be used instead..
        grp.add_argument('--savefolder', type=str, default=None, help=argparse.SUPPRESS)

        grp.add_argument('--savetiff', default='full',
                         choices=['crop', 'full', 'No'],
                         help="Option to save the reconstruction as tiff:\n\n"
                              "* ``crop``: only the scanned area\n"
                              "* ``full``: full reconstruction, with parts outside the scan area\n"
                              "* ``No``: don't save the tiff file")

        grp.add_argument('--savellk', action='store_true',
                         help="If you want to save the llk values in a separate text file, "
                              "which will be named 'everyllk.txt'")
        grp.add_argument('--encoder_coordinates', action='store_true',
                         help="Call this flag in order to use the encoder coordinates\n"
                         " instead of the written coordinates.")

        # VFN: the following parameters are automatically determined. Not sure they
        # should really be in self.params (they could be regular class members), but
        # we keep them here for now as they are needed

        # VFN: This should probably be available as an option in the main parser
        grp.add_argument('--logfile', action='store', type=str, default=p['logfile'],
                         help=argparse.SUPPRESS)

        return parser


def make_parser_sphinx():
    """Returns the argparse for sphinx documentation"""
    return PtychoRunnerHermes.make_parser(default_params)
