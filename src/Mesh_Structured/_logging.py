"""Logging utilities for the package."""

from __future__ import annotations

import logging


def get_default_logger(name: str = "Mesh_Structured") -> logging.Logger:
    """Create or retrieve a package logger."""

    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("[%(levelname)s] %(name)s - %(message)s"))
        logger.addHandler(handler)
    return logger
