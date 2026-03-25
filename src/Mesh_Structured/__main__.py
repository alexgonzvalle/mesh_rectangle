"""Command-line entry point for the package."""

from __future__ import annotations

import logging

from .mesh import MeshStructured


def main() -> None:
    """Log the public class exposed by the package."""

    logging.basicConfig(level=logging.INFO)
    logging.info("Mesh_Structured exports %s", MeshStructured.__name__)


if __name__ == "__main__":
    main()
