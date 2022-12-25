import fsspec
import zarr

fs = fsspec.filesystem('zip:///path/to/myfile.zip')


store = zarr.ZipStore('data.zip', mode='w')
root = zarr.group(store)
foo = root.create_group("foo")
    
foo = foo.zeros('aaa', shape=(10000, 10000), chunks=(100, 100), dtype='i4')
foo[:] = 10000

foo.flush()
store.close()

#opening the file is used in a with context

with fs.open('myfile.zip', mode='r') as f:
    print(root.info)
    

