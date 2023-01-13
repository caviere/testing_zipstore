import numpy as np
from osgeo import gdal
import zarr

def main():
    store = zarr.ZipStore('data.zip', mode='w')
    root = zarr.group(store)
    foo = root.create_group("foo")

    foo = foo.zeros('aaa', shape=(10000, 10000), chunks=(100, 100), dtype='i4')
    foo[:] = 10000
    store.close()
    
    # open the zarr store using the zarr driver
    ds = gdal.Open("/vsizip/data.zip")

    # create a dataset using the zarr driver
    foo_ds = gdal.GetDriverByName("ZARR").Create("foo_ds", 10000, 10000, 1)
    foo_ds.GetRasterBand(1).WriteArray(np.ones((10000, 10000)))
    foo_ds = None

if __name__ == "__main__":
    main()

