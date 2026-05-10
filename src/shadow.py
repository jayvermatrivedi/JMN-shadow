"""Shadow observables for the JMN configurations studied in the paper."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .metric import JMN1Spacetime, NakedSingularityMetric, SchwarzschildMetric


@dataclass(frozen=True)
class ShadowBoundary:
    """Circular shadow boundary in the observer sky."""

    radius: float

    def curve(self, num_points: int = 720) -> tuple[np.ndarray, np.ndarray]:
        """Return `(X, Y)` points for the circular boundary."""
        phi = np.linspace(0.0, 2.0 * np.pi, num_points, endpoint=False)
        return self.radius * np.cos(phi), self.radius * np.sin(phi)


def schwarzschild_shadow(metric: SchwarzschildMetric) -> ShadowBoundary:
    """Shadow radius set by the photon sphere."""
    return ShadowBoundary(radius=metric.critical_impact_parameter)


def jmn1_shadow(spacetime: JMN1Spacetime) -> ShadowBoundary:
    """For `M0 > 2/3`, the JMN1 shadow is inherited from the exterior photon sphere."""
    return ShadowBoundary(radius=spacetime.critical_impact_parameter)


def naked_singularity_shadow(metric: NakedSingularityMetric) -> ShadowBoundary:
    """Paper Eq. (24): the new naked singularity has critical `b_tp(r_tp=0) = M`."""
    return ShadowBoundary(radius=metric.mass)
