from pathlib import Path
import sys

import numpy as np
import xarray as xr

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from Mesh_Structured import CoordinateType, MeshStructured

ds = xr.open_dataset(r"D:\Development\Casos\CLIMPORT\Santander_Op\hindcast\2_Propagacion del oleaje (T3.2)\Batimetria.nc")
x, y, z = ds.lon.values, ds.lat.values, -ds.elevation.values[0]
x, y = np.meshgrid(x, y)

mesh = MeshStructured("Main", coord_type=CoordinateType.LONLAT)
mesh.execute(
    x,
    y,
    z,
    file_mesh_ini=r"D:\Development\Casos\CLIMPORT\Santander_Op\hindcast\2_Propagacion del oleaje (T3.2)\mesh_main.ini",
)
# mesh.save('Garachico/Bathymetry_mesh_main.dat')
mesh.plot()
