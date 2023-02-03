import zarr


def open_zipstore_with_zarr(filepath):
    try:
        with zarr.ZipStore(filepath, mode="r") as store:
            root = zarr.open_group(store, mode="r")
            # print(root.info)
        print("open with zarr:", "OK")
    except Exception as e:
        print("open with zarr:", e)


def open_zipstore_with_xarray(filepath):
    import xarray as xr

    try:
        with zarr.ZipStore(filepath, mode="r") as store:
            ds = xr.open_zarr(store, consolidated=False)
            # print(ds.compute())
        print("open with xarray:", "OK")
    except Exception as e:
        print("open with xarray:", e)


def open_zipstore_with_netcdf4(filepath):
    # there is no way to open zarr zipstore directly from the netcdf4 library
    import netCDF4 as nc

    try:
        ds = nc.Dataset(filepath, mode="r", format="NCZarr")
        ds.close()
        print("open with netcdf4:", "OK")
    except Exception as e:
        print("open with netcdf4:", e)


def open_zipstore_with_h5py(filepath):
    import h5py

    if h5py.is_hdf5(filepath):
        f = h5py.File(filepath, "r")
        f.close()
        print("open with h5py:", "OK")
    else:
        print("open with h5py:", "Not a valid HDFS file")


def open_zipstore_with_fsspec(filepath):
    import zarr.storage
    from zarr.storage import ZipStore

    try:
        store = zarr.storage.FSStore(
            url="", fs=ZipStore(path=filepath), mode="r"
        )
        z = zarr.open(store=store, path=filepath)
    except Exception as e:
        print("open with fsspec(ZipStore):", e)



def open_zipstore_with_gdal(filepath):
    from osgeo import gdal

    # full_filepath = f'ZARR:"{os.path.abspath(filepath)}"'

    ds = gdal.OpenEx(f'ZARR:{filepath}', gdal.OF_MULTIDIM_RASTER)
   
    assert ds is not None

def main():

    # from url: https://zenodo.org/record/5745520#.Y8qxtBxByV4
    filepath = "datasets/ESP0025722.zip"

    open_zipstore_with_zarr(filepath)

    open_zipstore_with_xarray(filepath)
    
    open_zipstore_with_netcdf4(filepath)

    open_zipstore_with_h5py(filepath)

    open_zipstore_with_fsspec(filepath)

    open_zipstore_with_gdal(filepath)

if __name__ == "__main__":
    main()
