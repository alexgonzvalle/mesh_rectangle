"""Plotting helpers for structured meshes."""

from __future__ import annotations

from pathlib import Path

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.axes import Axes

from .coordinates import CoordinateType


def _prepare_plot_values(z_values: np.ndarray) -> np.ndarray:
    plot_values = -np.array(z_values, dtype=float, copy=True)
    plot_values[plot_values >= 0] = np.nan
    return plot_values


def plot_bathymetry(
    x_values: np.ndarray,
    y_values: np.ndarray,
    z_values: np.ndarray,
    coordinate_type: CoordinateType | str,
    *,
    ax: Axes | None = None,
    output_path: str | Path | None = None,
    show: bool = True,
    dpi: int = 300,
) -> Axes:
    """Plot bathymetry on a 2D structured mesh."""

    normalized_type = CoordinateType.coerce(coordinate_type)
    plot_values = _prepare_plot_values(z_values)
    if ax is None:
        figure, ax = plt.subplots()
    else:
        figure = ax.figure

    ax.set_title("Bathymetry on structured mesh")
    if normalized_type is CoordinateType.UTM:
        ax.set_xlabel("X (m)")
        ax.set_ylabel("Y (m)")
    else:
        ax.set_xlabel("Longitude (deg)")
        ax.set_ylabel("Latitude (deg)")
    ax.set_aspect("equal")
    pcolor = ax.pcolor(
        x_values,
        y_values,
        plot_values,
        cmap="Blues_r",
        shading="auto",
        edgecolors="k",
        linewidth=0.5,
    )
    colorbar = figure.colorbar(pcolor, ax=ax)
    colorbar.set_label("Depth (m)")

    if output_path is not None:
        figure.savefig(output_path, dpi=dpi, bbox_inches="tight")
    if show:
        plt.show()
    return ax


def plot_bathymetry_3d(
    x_values: np.ndarray,
    y_values: np.ndarray,
    z_values: np.ndarray,
    coordinate_type: CoordinateType | str,
    *,
    ax: Axes | None = None,
    output_path: str | Path | None = None,
    show: bool = True,
    dpi: int = 300,
) -> Axes:
    """Plot bathymetry on a 3D structured mesh."""

    normalized_type = CoordinateType.coerce(coordinate_type)
    plot_values = _prepare_plot_values(z_values)

    if ax is None:
        figure = plt.figure()
        ax = figure.add_subplot(111, projection="3d")
        ax.view_init(50, 135)
    else:
        figure = ax.figure

    ax.plot_surface(x_values, y_values, plot_values, cmap="Blues_r")
    if normalized_type is CoordinateType.UTM:
        ax.set_xlabel("X (m)")
        ax.set_ylabel("Y (m)")
    else:
        ax.set_xlabel("Longitude (deg)")
        ax.set_ylabel("Latitude (deg)")
    ax.set_zlabel("Depth (m)")

    if output_path is not None:
        figure.savefig(output_path, dpi=dpi, bbox_inches="tight")
    if show:
        plt.show()
    return ax
