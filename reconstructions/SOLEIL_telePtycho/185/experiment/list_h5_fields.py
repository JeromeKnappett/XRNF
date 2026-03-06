import h5py
import sys

filename = sys.argv[1]  # HDF5 file path given as command line argument

with h5py.File(filename, 'r') as f:
    def print_name(name, obj):
        if isinstance(obj, h5py.Dataset):
            print(name)
    f.visititems(print_name)
