import netCDF4 as nc
import xarray as xr
import zarr


nc_file = nc.Dataset('data.nc', 'w', format='NETCDF4')

foo_group = nc_file.createGroup("foo")
bar_group = nc_file.createGroup("bar")

dim = nc_file.createDimension('dim', 10000)

foo = nc_file.createVariable('aaa', 'i4', ('dim', 'dim'), chunksizes=(100,100))

bar = nc_file.createVariable('bbb', 'i4', ('dim', 'dim'), chunksizes=(100, 100))

foo[:,:] = 10000

bar[:,:] = 10000

nc_file.close()

nc_file = xr.open_dataset('data.nc')

store = zarr.ZipStore('data.zip', mode='w')

zarr = nc_file.to_zarr('data.zarr', store)

nc_file.close()
store.close()
