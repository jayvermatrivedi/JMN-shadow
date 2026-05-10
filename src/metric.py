"""Metric definitions for static, spherically symmetric spacetimes.

The paper uses the generic line element

    ds^2 = -g_tt(r) dt^2 + g_rr(r) dr^2 + r^2 dOmega^2

for the null-geodesic and radiative-transfer analysis.  In the Mathematica
notebook the same objects are stored as `Aint`, `Aext`, `Bint`, and `Bext`.
Here:

`g_tt(r)` is the positive lapse factor appearing in front of `dt^2`, and
`g_rr(r)` is the radial metric coefficient.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

import numpy as np


class StaticSphericalMetric(Protocol):
    """Protocol for metrics used by the ray-tracing code."""

    def g_tt(self, r: float) -> float:
        """Return the positive metric function g_tt(r)."""

    def g_rr(self, r: float) -> float:
        """Return the radial metric function g_rr(r)."""


@dataclass(frozen=True)
class SchwarzschildMetric:
    """Schwarzschild spacetime written in the paper's convention.

    The metric is

        ds^2 = -(1 - 2M/r) dt^2 + (1 - 2M/r)^(-1) dr^2 + r^2 dOmega^2.
    """

    mass: float = 1.0

    @property
    def horizon_radius(self) -> float:
        """Schwarzschild radius `r = 2M`."""
        return 2.0 * self.mass

    @property
    def photon_sphere_radius(self) -> float:
        """Photon-sphere radius `r_ph = 3M`."""
        return 3.0 * self.mass

    @property
    def critical_impact_parameter(self) -> float:
        """Critical impact parameter `b_ph = 3 sqrt(3) M`."""
        return 3.0 * np.sqrt(3.0) * self.mass

    def g_tt(self, r: float) -> float:
        return 1.0 - 2.0 * self.mass / r

    def g_rr(self, r: float) -> float:
        return 1.0 / self.g_tt(r)


@dataclass(frozen=True)
class JMN1Spacetime:
    """JMN1 naked-singularity spacetime matched to an exterior Schwarzschild region.

    Paper Eq. (19) gives the interior metric

        ds^2 = -(1 - M0) (r / R_b)^(M0 / (1 - M0)) dt^2
               + dr^2 / (1 - M0)
               + r^2 dOmega^2,

    and the exterior Schwarzschild mass satisfies

        M_T = M0 R_b / 2.

    The Mathematica notebook uses:
    - `M0 = 0.7`
    - `rb = 2 / M0`
    which implies `M_T = 1`.
    """

    m0: float = 0.7
    rb: float | None = None

    def __post_init__(self) -> None:
        if not (0.0 < self.m0 < 1.0):
            raise ValueError("m0 must lie in (0, 1).")
        object.__setattr__(self, "rb", 2.0 / self.m0 if self.rb is None else self.rb)

    @property
    def exterior_mass(self) -> float:
        """Exterior Schwarzschild mass `M_T = M0 R_b / 2`."""
        return 0.5 * self.m0 * self.rb

    @property
    def exponent(self) -> float:
        """Power `M0 / (1 - M0)` appearing in the interior lapse."""
        return self.m0 / (1.0 - self.m0)

    @property
    def photon_sphere_radius(self) -> float:
        """Photon-sphere radius of the exterior Schwarzschild region."""
        return 3.0 * self.exterior_mass

    @property
    def critical_impact_parameter(self) -> float:
        """Critical impact parameter inherited from the exterior photon sphere."""
        return 3.0 * np.sqrt(3.0) * self.exterior_mass

    def interior_g_tt(self, r: float) -> float:
        return (1.0 - self.m0) * (r / self.rb) ** self.exponent

    def interior_g_rr(self, r: float) -> float:
        return 1.0 / (1.0 - self.m0)

    def exterior_g_tt(self, r: float) -> float:
        return 1.0 - 2.0 * self.exterior_mass / r

    def exterior_g_rr(self, r: float) -> float:
        return 1.0 / self.exterior_g_tt(r)


@dataclass(frozen=True)
class NakedSingularityMetric:
    """Asymptotically flat naked singularity introduced in paper Eq. (1).

    The metric is

        ds^2 = -(r / (M + r))^2 dt^2 + (1 + M / r)^2 dr^2 + r^2 dOmega^2.
    """

    mass: float = 1.0

    def g_tt(self, r: float) -> float:
        return (r / (self.mass + r)) ** 2

    def g_rr(self, r: float) -> float:
        return (1.0 + self.mass / r) ** 2
