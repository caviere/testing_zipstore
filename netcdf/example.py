import zarr


def list_methods(obj):
    for attr in dir(obj):
        if attr.startswith("_"):
            continue
        print(attr)


def open_zipstore_with_zarr(filepath):
    with zarr.ZipStore(filepath, mode="r") as store:
        root = zarr.open_group(store, mode="r")
        print(root.info)


def open_zipstore_with_xarray(filepath):
    import xarray as xr

    with zarr.ZipStore(filepath, mode="r") as store:
        ds = xr.open_zarr(store, consolidated=False)
        print(ds.compute())


def open_zipstore_with_netcdf4(filepath):
    # there is no way to open zarr zipstore directly from the netcdf4 library
    import netCDF4 as nc

    try:
        ds = nc.Dataset(filepath, mode="r", format="NCZarr")
        ds.close()
    except Exception as e:
        pass


def main():

    # from url: https://zenodo.org/record/5745520#.Y8qxtBxByV4
    filepath = "datasets/ESP0025722.zip"

    # open_zipstore_with_zarr(filepath)

    # open_zipstore_with_xarray(filepath)

    open_zipstore_with_netcdf4(filepath)


if __name__ == "__main__":
    main()
