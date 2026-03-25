"""Interpolation utilities used by structured meshes."""

from __future__ import annotations

import numpy as np
from scipy.spatial import Delaunay

from ._validation import as_float_array, validate_matching_shapes


def interpolation_weights(
    source_points: np.ndarray,
    target_points: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Compute barycentric interpolation weights."""

    triangulation = Delaunay(source_points)
    simplex = triangulation.find_simplex(target_points)
    vertices = np.full((target_points.shape[0], source_points.shape[1] + 1), -1, dtype=int)
    weights = np.full((target_points.shape[0], source_points.shape[1] + 1), np.nan, dtype=float)

    valid = simplex >= 0
    if np.any(valid):
        simplex_indices = simplex[valid]
        vertices[valid] = triangulation.simplices[simplex_indices]
        transforms = triangulation.transform[simplex_indices]
        delta = target_points[valid] - transforms[:, source_points.shape[1]]
        barycentric = np.einsum("nij,nj->ni", transforms[:, : source_points.shape[1], :], delta)
        weights[valid] = np.hstack((barycentric, 1 - barycentric.sum(axis=1, keepdims=True)))

    return vertices, weights


def apply_interpolation_weights(values: np.ndarray, vertices: np.ndarray, weights: np.ndarray) -> np.ndarray:
    """Apply barycentric interpolation weights to source values."""

    result = np.full(weights.shape[0], np.nan, dtype=float)
    valid = np.all(vertices >= 0, axis=1) & np.all(np.isfinite(weights), axis=1)
    if np.any(valid):
        result[valid] = np.einsum("ij,ij->i", np.take(values, vertices[valid]), weights[valid])
    return result


def interpolate_to_mesh(
    x_mesh: np.ndarray,
    y_mesh: np.ndarray,
    x_values: np.ndarray,
    y_values: np.ndarray,
    values: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Interpolate scattered values onto a structured mesh."""

    x_values = as_float_array(x_values, name="x_values")
    y_values = as_float_array(y_values, name="y_values")
    values = as_float_array(values, name="values")
    validate_matching_shapes(
        names=("x_values", "y_values", "values"),
        arrays=(x_values, y_values, values),
    )

    source_points = np.column_stack((x_values.ravel(), y_values.ravel()))
    target_points = np.column_stack((x_mesh.ravel(), y_mesh.ravel()))
    vertices, weights = interpolation_weights(source_points, target_points)
    interpolated = apply_interpolation_weights(values.ravel(), vertices, weights)
    return x_mesh, y_mesh, interpolated.reshape(x_mesh.shape)
