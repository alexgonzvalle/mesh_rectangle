"""Input and output helpers for configuration and bathymetry grids."""

from __future__ import annotations

import configparser
from pathlib import Path

import numpy as np

from ._grid import MeshDefinition
from .coordinates import CoordinateType, get_coordinate_parameter_names


def read_mesh_definition(
    configuration_path: str | Path,
    *,
    key: str,
    coordinate_type: CoordinateType | str,
) -> MeshDefinition:
    """Read a mesh definition from an INI configuration file."""

    path = Path(configuration_path)
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {path}")

    parser = configparser.ConfigParser()
    parser.read(path)
    if key not in parser:
        raise KeyError(f"Section {key!r} was not found in {path}.")

    section = parser[key]
    x_name, y_name, dx_name, dy_name, nx_name, ny_name = get_coordinate_parameter_names(coordinate_type)
    required_names = (x_name, y_name, dx_name, dy_name, nx_name, ny_name)
    missing = [name for name in required_names if name not in section]
    if missing:
        raise ValueError(f"Missing mesh parameters in {path}: {', '.join(missing)}.")

    return MeshDefinition(
        xmin=float(section[x_name]),
        ymin=float(section[y_name]),
        dx=float(section[dx_name]),
        dy=float(section[dy_name]),
        nx=int(section[nx_name]),
        ny=int(section[ny_name]),
    )


def write_mesh_definition(
    configuration_path: str | Path,
    *,
    key: str,
    coordinate_type: CoordinateType | str,
    definition: MeshDefinition,
) -> None:
    """Write a mesh definition to an INI configuration file."""

    path = Path(configuration_path)
    x_name, y_name, dx_name, dy_name, nx_name, ny_name = get_coordinate_parameter_names(coordinate_type)
    with path.open("w", encoding="utf-8") as stream:
        stream.write(f"[{key}]\n")
        stream.write(f"{x_name} = {definition.xmin}\n")
        stream.write(f"{y_name} = {definition.ymin}\n")
        stream.write(f"{dx_name} = {definition.dx}\n")
        stream.write(f"{dy_name} = {definition.dy}\n")
        stream.write(f"{nx_name} = {definition.nx}\n")
        stream.write(f"{ny_name} = {definition.ny}\n")


def save_bathymetry_grid(output_path: str | Path, z_values: np.ndarray) -> None:
    """Save a 2D bathymetry array to the legacy tab-separated format."""

    array = np.asarray(z_values, dtype=float)
    with Path(output_path).open("w", encoding="utf-8") as stream:
        for row in array:
            serialized_row = [
                "NaN" if np.isnan(value) or value == 0 else f"{value:5.6f}" for value in row
            ]
            stream.write("\t".join(serialized_row))
            stream.write("\n")


def load_bathymetry_grid(input_path: str | Path) -> np.ndarray:
    """Load a bathymetry array stored in the legacy tab-separated format."""

    rows: list[list[float]] = []
    with Path(input_path).open("r", encoding="utf-8") as stream:
        for line in stream:
            values = line.strip().split("\t")
            rows.append([np.nan if value in {"", "NaN"} else float(value) for value in values if value != ""])

    if not rows:
        raise ValueError(f"Bathymetry file {input_path} is empty.")

    row_lengths = {len(row) for row in rows}
    if len(row_lengths) != 1:
        raise ValueError(f"Bathymetry file {input_path} contains rows with inconsistent lengths.")

    return np.asarray(rows, dtype=float)
