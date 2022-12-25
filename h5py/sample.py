
import zarr
import h5py


store = zarr.ZipStore('data.zip', mode='w')

root = zarr.group(store)

foo = root.create_group("foo")
bar = root.create_group("bar")

foo = foo.zeros('aaa', shape=(10000, 10000), chunks=(100, 100), dtype='i4')
bar = bar.zeros('bbb', shape=(10000, 10000), chunks=(100, 100), dtype='i4')

foo[:] = 10000
bar[:] = 10000

store.close()

if h5py.is_hdf5('data.zip'):
    
    h5f = h5py.File('data.zip', 'w')

    foo_ds = h5f.create_dataset("foo/aaa", data=foo)
    bar_ds = h5f.create_dataset("bar/bbb", data=bar)

    foo_data = foo_ds[:]
    bar_data = bar_ds[:]

    h5f.close()
else:
    print("The file is not a valid HDF5 file.")
