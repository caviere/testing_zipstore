import numpy as np
import sys
from osgeo import ogr
import zarr


driver = ogr.GetDriverByName('ZARR')

if driver is None:
    print("Error: Could not find the ZARR driver")
    sys.exit()
    
store = zarr.ZipStore('data.zip', mode='w')

root = zarr.group(store)
foo = root.create_group("foo")

foo = foo.zeros('aaa', shape=(100, 100), chunks=(10, 10), dtype='i4')

foo[:] = 100
store.close()

ds = ogr.Open('data.zip')
foo_ds = driver.Create("/foo/aaa", 100, 100, 1, ogr.GDT_Int32)
foo_ds.WriteArray(np.ones((100, 100)))

foo_ds = None
