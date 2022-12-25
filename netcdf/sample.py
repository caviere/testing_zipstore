import netCDF4 as nc
import xarray as xr
import numpy as np
import zarr

nc_file = xr.Dataset(
    data_vars={
        'foo': (('dim', 'dim'), np.full((10000, 10000), 10000)),
        'bar': (('dim', 'dim'), np.full((10000, 10000), 10000))
    },
    coords={
        'dim': range(10000)
    }
)

store = zarr.ZipStore('data.zip', mode='w')

encoding ={'foo': {'chunks': (100,100)}, 'bar': {'chunks': (100,100)}}

zarr_group = nc_file.to_zarr(store, encoding=encoding)

store.close()

store = zarr.ZipStore('data.zip', mode='r')

zarr_group = zarr.open_group(store)

print(nc_file.foo)

nc_file.close()

store.close()
