"""Coordinate system definitions and related helpers."""

from __future__ import annotations

from enum import Enum


class CoordinateType(str, Enum):
    """Supported coordinate conventions for structured meshes."""

    LONLAT = "LONLAT"
    UTM = "UTM"
    WORLD_MERCATOR = "WorldMercator"

    @classmethod
    def coerce(cls, value: "CoordinateType | str") -> "CoordinateType":
        """Convert a string or enum value into a :class:`CoordinateType`."""

        if isinstance(value, cls):
            return value

        for candidate in cls:
            if candidate.value == value:
                return candidate

        supported = ", ".join(member.value for member in cls)
        raise ValueError(f"Unsupported coordinate type {value!r}. Expected one of: {supported}.")


def get_coordinate_parameter_names(
    coordinate_type: CoordinateType | str,
) -> tuple[str, str, str, str, str, str]:
    """Return configuration parameter names for a coordinate convention."""

    normalized_type = CoordinateType.coerce(coordinate_type)
    if normalized_type is CoordinateType.UTM:
        return "xmin", "ymin", "dx", "dy", "nx", "ny"
    return "lonmin", "latmin", "dlon", "dlat", "nlon", "nlat"
