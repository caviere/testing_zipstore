import fsspec
import zarr

fs = fsspec.filesystem('zip:///path/to/myfile.zip')


store = zarr.ZipStore('data.zip', mode='w')
root = zarr.group(store)
foo = root.create_group("foo")
    
foo = foo.zeros('aaa', shape=(100, 100), chunks=(10, 10), dtype='i4')
foo[:] = 100

foo.flush()
store.close()

#opening the file is used in a with context

with fs.open('myfile.zip', mode='r') as f:
    print(root.info)
    

