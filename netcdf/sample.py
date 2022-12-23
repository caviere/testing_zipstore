import netCDF4 as nc
import xarray as xr
import zarr


nc_file = nc.Dataset('data.nc', 'w', format='NETCDF4')

foo_group = nc_file.createGroup("foo")
bar_group = foo_group.createGroup("bar")

dim = nc_file.createDimension('dim', 100)

foo = nc_file.createVariable('aaa', 'i4', ('dim', 'dim'), chunksizes=(10,10))

bar = nc_file.createVariable('bbbr', 'i4', ('dim', 'dim'),chunksizes=(10,10))

foo[:,:] = 100

bar[:,:] = 100

nc_file.close()

nc_file = xr.open_dataset('data.nc')

store = zarr.ZipStore('data.zip', mode='w')

zarr = nc_file.to_zarr('data.zarr', store)

nc_file.close()
store.close()
