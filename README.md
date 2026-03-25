# mesh_rectangle

`mesh_rectangle` is a scientific Python library for building regular rectangular meshes and interpolating bathymetry or other scalar fields onto them.

The project is structured as an installable `src` package with a focused public API and explicit validation.

## Installation

```bash
pip install git+https://github.com/user/repository.git
```

For local development:

```bash
pip install -e .[dev]
```

## Dependencies

- `numpy`
- `scipy`
- `matplotlib`

## Minimal example

```python
import numpy as np

from mesh_rectangle import MeshStructured

xb = np.array([0.0, 1.0, 0.0, 1.0, 0.5])
yb = np.array([0.0, 0.0, 1.0, 1.0, 0.5])
zb = np.array([-1.0, -2.0, -3.0, -4.0, -2.5])

mesh = MeshStructured("main")
mesh.execute(xb, yb, zb, x1=0.0, x2=1.0, y1=0.0, y2=1.0, dx=0.5, dy=0.5)
mesh.save_z("bathymetry.dat")
mesh.plot(_show=False)
```

## Public API

- `mesh_rectangle.MeshStructured`
- `mesh_rectangle.CoordinateType`

## Testing

Run the test suite with:

```bash
pytest
```

A reasonable near-term target for this project is at least 90% coverage over the public computational and IO paths.
