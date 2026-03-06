"""Generate zone plate to scale for lithography manufacturing.

Example usage: 

>>> # Create a 140 mm focal length zone plate for 625nm light where
>>> # the lithographer is accurate to 10160 dpi.

>>> from zone_plate import NormalFZP

>>> zp = NormalFZP(f=140, w=625, thinnest_zone=25.4/10160)

>>> # Preview the zone plate.

>>> zp.plot()

>>> # Rendering high DPI will take a long time or fail, so only set it
>>> # when saving directly to disk.

>>> zp.plot(save=True, dpi=10160)


License: Public Domain

Author: Pariksheet Nanda <omsai@member.fsf.org> 2014-08-10

"""
import numpy as np
import matplotlib.pyplot as plt

_DEBUG = False

"""This NormalZFP class below has been adapted from the xrt package.
In keeping with the MIT license, below are the copyright and
permissions notices of the xrt package:

Copyright (c) 2014 Konstantin Klementiev, Roman Chernikov

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

"""


class NormalFZP(object):
    """Implements a circular Fresnel Zone Plate, as it is described in
    X-Ray Data Booklet, Section 4.4.
    """

    def __init__(self, *args, **kwargs):
        """*f* (mm) is the focal distance calculated for wavelength *w*
        (nm). The number of zones is given either by *N* or calculated
        from *thinnest_zone* (mm). If *is_central_zone_black* is False,
        the zones are inverted. The diffraction order (can be a
        sequence) is given by *order*.

        """
        self.__pop_kwargs(**kwargs)

    def __pop_kwargs(self, **kwargs):
        from scipy import interpolate

        f = kwargs.pop("f")
        w = kwargs.pop("w")
        N = kwargs.pop("N", 1000)
        self.is_central_zone_black = kwargs.pop("is_central_zone_black", True)
        thinnest_zone = kwargs.pop("thinnest_zone", None)
        wavelength = w * 1e-6  # mm
        if thinnest_zone is not None:
            N = wavelength * f / 4.0 / thinnest_zone**2
        self.zones = np.arange(N + 1)
        self.rn = np.sqrt(
            self.zones * f * wavelength + 0.25 * (self.zones * wavelength) ** 2
        )
        if _DEBUG:
            print(self.rn)
            print(f, N)
            print("R(N)={0}, dR(N)={1}".format(self.rn[-1], self.rn[-1] - self.rn[-2]))
        self.r_to_i = interpolate.interp1d(
            self.rn, self.zones, bounds_error=False, fill_value=0
        )
        self.i_to_r = interpolate.interp1d(
            self.zones, self.rn, bounds_error=False, fill_value=0
        )
        return kwargs

    def get_patch_collection(self):
        """Patch collection of circles for plotting the zone plate.  The idea
        to use patches:
        http://matplotlib.org/examples/api/patch_collection.html

        """
        from matplotlib.patches import Circle
        from matplotlib.collections import PatchCollection

        patches = []
        zone = 1
        # Plot largest to smallest radius by reversing rn, so that the
        # zorder is automatically incremented.
        for radius in self.rn[-1::-1]:
            if self.is_central_zone_black and (zone % 2):
                facecolor = "black"
            else:
                facecolor = "white"
            patches.append(
                Circle((0, 0), radius, edgecolor="none", facecolor=facecolor)
            )
            zone += 1
        return PatchCollection(patches, match_original=True)

    def plot(self, mask_lining=5, dpi=80, save=False, file_ext="svg"):
        """Scaled plot of the zone plate.  *mask_lining* (mm) is the extra
        blacked out area around the zone plate that allows us to image
        out to the edges.

        """
        r = self.rn[-1]  # mm
        d = (2.0 * r + 60) / 25.4  # inches
        s = d + mask_lining * 2.0 / 25.4

        # The figure facecolor is actually the background.  Yes, it's
        # confusing.
        fig = plt.figure(figsize=(s, s), dpi=dpi, facecolor="white")
        axes = fig.add_subplot(111, aspect=1)  # , axisbg="black")
        p = self.get_patch_collection()
        axes.add_collection(p)
        # Patches are not data, so the plot does not resize to fit
        # them.  Therefore we have to specify the axes coordinates.
        rp = r + 0.01  # + mask_lining     # Add mask width to padding.
        plt.axis([-rp, rp, -rp, rp])
        # Fill the entire figure area.
        #        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
        if not save:
            plt.show()
        else:
            print("Saving figure...")
            fig.savefig(
                "zone_plates-dpi{0}-radius{1:.2f}mm-{2:.2f}x{2:.2f}inches.{3}".format(
                    dpi, self.rn[-1], s, file_ext
                ),
                format=file_ext,
                facecolor="white",
            )
            print("... Done.")
        # Release memory.
        plt.close()
        return p


def fzp1D(wl, r, f, num_data=1024):
    """
    Parameters
    ----------
    wl : wavelength in nm.
    r : radius in um.
    f : focal length in mm.
    num_data : TYPE, optional
        DESCRIPTION. The default is 1024.

    Returns
    -------
    fzp.

    """
    from diffractio import degrees, mm, np, plt, um, nm
    from diffractio.scalar_masks_X import Scalar_mask_X

    from numpy import loadtxt
    import matplotlib

    matplotlib.rcParams["figure.dpi"] = 125

    num_data = 1024
    length = (2 * r + 50) * um
    x = np.linspace(-length / 2, length / 2, num_data)
    wavelength = wl * nm
    t1 = Scalar_mask_X(x, wavelength)
    fzp = t1.fresnel_lens(
        x0=0 * um, radius=r * um, focal=f * mm, mask=True, kind="amplitude", phase=np.pi
    )
    t1.draw(kind="amplitude")

    return fzp


if __name__ == "__main__":
    # Plot a pair of 10.88mm focusing zone plates for 6.7nm and 13.5nm incident
    # wavelength with white space in between.
    print("Generating plates...")
    zp1 = NormalFZP(f=10.888, w=6.7, N=1666.666)
    zp2 = NormalFZP(f=10.888, w=13.5, N=1666.666)
    print("... Done.")
    #    mask_lining = 5             # mm
    dpi = 506
    save = False  # Whether to write to file.
    outline_only = False  # Don't render the plates.  Useful to
    # check sizing.
    file_ext = "ps"

    zps = [zp1, zp2]

    # Padding should be a minimum of 5mm.  Find the zone plate with
    # the largest diameter, and calculate the padded radius to use in
    # the zone plate subplots.
    max_rn = max(zp1.rn[-1], zp2.rn[-1])
    rp = np.ceil(max_rn)  # + 0.001)    # Padded radius.

    # Set Figure size.
    side_mm = 2 * rp * 60.2  # 0.2 from fig.subplotpars.wspace.
    side_in = side_mm / 25.4
    # The figure facecolor is actually the background.  Yes, it's
    # confusing.
    fig = plt.figure(dpi=dpi, facecolor="white", figsize=(side_in, side_in))

    if outline_only:
        axisbg = "white"
    else:
        axisbg = "black"

    print("Filling subplots...")
    subplot = 0
    for zp in zps:
        subplot += 1
        axes = fig.add_subplot(220 + subplot, aspect=1)  # , axisbg=axisbg)
        if not outline_only:
            axes.add_collection(zp.get_patch_collection())
        # Patches are not data, so the plot does not resize to fit
        # them.  Therefore we have to specify the axes coordinates.
        plt.axis([-rp, rp, -rp, rp])

        # Get rid of the subplot internal padding.
        fig.subplotpars.left = 0
        fig.subplotpars.right = 1
        fig.subplotpars.bottom = 0
        fig.subplotpars.top = 1

        # Fill the entire figure area.
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    print("... Done.")

    if save:
        print("Saving figure...")
        # TODO: Tie filename to __repr__, etc.
        fig.savefig(
            "zone_plates-dpi{0}-radii({1:.2f},{2:.2f})mm-sheet{3:.2f}x{3:.2f}inches.{4}".format(
                dpi, zp1.rn[-1], zp2.rn[-1], side_in, file_ext
            ),
            format=file_ext,
            facecolor="white",
        )
        print("... Done.")
    else:
        plt.show()

    # Release memory.
    plt.close()
