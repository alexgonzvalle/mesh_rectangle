import xarray as xr
import numpy as np
from MeshStructured.MeshStructured import MeshStructured

ds = xr.open_dataset(r'D:\Development\Casos\CLIMPORT\Santander_Op\hindcast\2_Propagacion del oleaje (T3.2)\Batimetria.nc')
x, y, z = ds.lon.values, ds.lat.values, -ds.elevation.values[0]
x, y = np.meshgrid(x, y)

mesh = MeshStructured('Main', coord_type='LONLAT')
mesh.execute(x, y, z, file_mesh_ini=r'D:\Development\Casos\CLIMPORT\Santander_Op\hindcast\2_Propagacion del oleaje (T3.2)\mesh_main.ini')
# mesh.save('Garachico/Bathymetry_mesh_main.dat')
mesh.plot()
