import numpy as np
import sys
from osgeo import ogr
import zarr


driver = ogr.GetDriverByName('ZARR')
    
store = zarr.ZipStore('data.zip', mode='w')

root = zarr.group(store)
foo = root.create_group("foo")

foo = foo.zeros('aaa', shape=(10000, 10000), chunks=(100, 100), dtype='i4')

foo[:] = 10000
store.close()

ds = ogr.Open('data.zip')
foo_ds = driver.Create("/foo/aaa", 10000, 10000, 1, ogr.GDT_Int32)
foo_ds.WriteArray(np.ones((10000, 10000)))

foo_ds = None
