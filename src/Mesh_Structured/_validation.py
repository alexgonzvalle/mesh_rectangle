"""Validation helpers for public APIs."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import numpy as np


def as_float_array(values: Iterable[float], *, name: str) -> np.ndarray:
    """Convert an iterable into a NumPy array of floats."""

    array = np.asarray(values, dtype=float)
    if array.size == 0:
        raise ValueError(f"{name} must contain at least one value.")
    return array


def validate_matching_shapes(*, names: tuple[str, ...], arrays: tuple[np.ndarray, ...]) -> None:
    """Validate that all arrays share the same shape."""

    first_shape = arrays[0].shape
    for name, array in zip(names[1:], arrays[1:]):
        if array.shape != first_shape:
            joined_names = ", ".join(names)
            raise ValueError(
                f"{joined_names} must share the same shape. "
                f"Expected {first_shape}, received {name}={array.shape}."
            )


def validate_positive(value: float, *, name: str) -> None:
    """Require a strictly positive scalar value."""

    if value <= 0:
        raise ValueError(f"{name} must be greater than zero. Received {value}.")


def validate_sampling_fraction(value: float) -> None:
    """Require a sampling fraction in the interval ``(0, 1]``."""

    if value <= 0 or value > 1:
        raise ValueError(
            f"factor_select must be within the interval (0, 1]. Received {value}."
        )


def ensure_path_exists(path: str | Path) -> Path:
    """Return a path and ensure the referenced file exists."""

    candidate = Path(path)
    if not candidate.exists():
        raise FileNotFoundError(f"File not found: {candidate}")
    return candidate
