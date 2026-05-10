"""Numerical utilities shared by the JMN ray-tracing modules."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq


DEFAULT_QUAD_LIMIT = 300
DEFAULT_QUAD_EPSABS = 1.0e-10
DEFAULT_QUAD_EPSREL = 1.0e-8


@dataclass(frozen=True)
class IntegrationConfig:
    """Configuration for one-dimensional quadrature."""

    epsabs: float = DEFAULT_QUAD_EPSABS
    epsrel: float = DEFAULT_QUAD_EPSREL
    limit: int = DEFAULT_QUAD_LIMIT


def safe_sqrt(value: float, *, tol: float = 1.0e-12) -> float:
    """Square root with a small tolerance for negative roundoff."""
    if value < -tol:
        raise ValueError(f"Encountered negative quantity under square root: {value}")
    return float(np.sqrt(max(value, 0.0)))


def quad_real(func: Callable[[float], float], a: float, b: float, *, config: IntegrationConfig) -> float:
    """Integrate the real-valued function `func` between `a` and `b`."""
    value, _ = quad(func, a, b, epsabs=config.epsabs, epsrel=config.epsrel, limit=config.limit)
    return float(np.real(value))


def find_outer_turning_point(
    impact_parameter: float,
    g_tt: Callable[[float], float],
    photon_sphere_radius: float,
    r_max: float,
) -> float:
    """Solve `r / sqrt(g_tt(r)) = b` for the outer turning point.

    For the Schwarzschild exterior and `b > b_crit`, the relevant turning point
    for a ray arriving from infinity is the root outside the photon sphere.
    """

    def equation(r: float) -> float:
        return r / np.sqrt(g_tt(r)) - impact_parameter

    left = photon_sphere_radius * (1.0 + 1.0e-8)
    right = max(r_max, impact_parameter * 2.0)

    # Expand the bracket if needed.  For the cases used here the outer root is
    # always well below this cap.
    while equation(right) < 0.0:
        right *= 2.0
        if right > 1.0e7:
            raise RuntimeError("Failed to bracket the outer turning point.")

    return float(brentq(equation, left, right))
