import h5py
import sys

filename, field = sys.argv[1], sys.argv[2]  # file and dataset name

with h5py.File(filename, 'r') as f:
	try:
		print(f[field][:])
		print('shape')
		print(f[field][0].shape)
	except:
		print(f[field][()])
