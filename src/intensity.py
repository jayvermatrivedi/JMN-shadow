"""Observed intensity and emissivity prescriptions from the paper."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .geodesics import radial_null_momentum, redshift_factor
from .metric import JMN1Spacetime, SchwarzschildMetric
from .utils import IntegrationConfig, find_outer_turning_point, quad_real


@dataclass(frozen=True)
class RadiativeTransferConfig:
    """Settings for the line-of-sight intensity integrals."""

    r_observer: float = 50.0
    r_min_interior: float = 1.0e-8
    integration: IntegrationConfig = IntegrationConfig()


def monochromatic_emissivity(r: float) -> float:
    """Paper Eq. (26): emissivity scales as `j(nu_e) propto delta(nu_e - nu_*) / r^2`.

    After integrating over frequency, the only radial dependence that remains is
    the `1 / r^2` factor.
    """

    return 1.0 / (r * r)


def line_integrand(g_tt: float, g_rr: float, r: float, impact_parameter: float, *, outgoing: bool) -> float:
    """Integrand used in the notebook for Eq. (32).

    The Mathematica notebook defines

        Intredshift    :=  (g_red)^3  * A / r^2 * 1 / k^r
        Intblueshift   := -(g_blue)^3 * A / r^2 * 1 / k^r

    and the same structure is used for the JMN interior.
    """

    g_factor = redshift_factor(g_tt, g_rr, r, impact_parameter, outgoing=outgoing)
    kr = radial_null_momentum(g_tt, g_rr, r, impact_parameter)
    prefactor = g_tt * monochromatic_emissivity(r) / kr
    return prefactor * g_factor**3 if outgoing else -prefactor * g_factor**3


def jmn1_intensity(impact_parameter: float, spacetime: JMN1Spacetime, config: RadiativeTransferConfig) -> float:
    """Observed intensity for the JMN1 configuration used in Figure 2(c)/(d).

    This matches the notebook branching:

    - for `b < b_crit`: integrate the interior and exterior outgoing branch
    - for `b >= b_crit`: integrate incoming plus outgoing exterior branches
    """

    b_crit = spacetime.critical_impact_parameter
    integration = config.integration

    if impact_parameter < b_crit:
        interior = quad_real(
            lambda r: line_integrand(
                spacetime.interior_g_tt(r),
                spacetime.interior_g_rr(r),
                r,
                impact_parameter,
                outgoing=True,
            ),
            config.r_min_interior,
            spacetime.rb,
            config=integration,
        )
        exterior = quad_real(
            lambda r: line_integrand(
                spacetime.exterior_g_tt(r),
                spacetime.exterior_g_rr(r),
                r,
                impact_parameter,
                outgoing=True,
            ),
            spacetime.rb,
            config.r_observer,
            config=integration,
        )
        return interior + exterior

    turning_point = find_outer_turning_point(
        impact_parameter,
        spacetime.exterior_g_tt,
        spacetime.photon_sphere_radius,
        config.r_observer,
    )

    incoming = quad_real(
        lambda r: line_integrand(
            spacetime.exterior_g_tt(r),
            spacetime.exterior_g_rr(r),
            r,
            impact_parameter,
            outgoing=False,
        ),
        config.r_observer,
        turning_point,
        config=integration,
    )
    outgoing = quad_real(
        lambda r: line_integrand(
            spacetime.exterior_g_tt(r),
            spacetime.exterior_g_rr(r),
            r,
            impact_parameter,
            outgoing=True,
        ),
        turning_point,
        config.r_observer,
        config=integration,
    )
    return incoming + outgoing


def schwarzschild_intensity(
    impact_parameter: float,
    metric: SchwarzschildMetric,
    config: RadiativeTransferConfig,
) -> float:
    """Observed intensity for Schwarzschild spacetime.

    This uses the same exterior branch structure as the Mathematica notebook:

    - for `b < b_crit`, only the outgoing branch from the horizon-near region to
      the observer contributes
    - for `b >= b_crit`, the ray has an outer turning point and the incoming plus
      outgoing branches both contribute

    The paper's Schwarzschild panels use `M_T = 1`, so the horizon is at `r=2`.
    """

    b_crit = metric.critical_impact_parameter
    integration = config.integration
    horizon_floor = metric.horizon_radius * (1.0 + 1.0e-8)

    if impact_parameter < b_crit:
        return quad_real(
            lambda r: line_integrand(
                metric.g_tt(r),
                metric.g_rr(r),
                r,
                impact_parameter,
                outgoing=True,
            ),
            horizon_floor,
            config.r_observer,
            config=integration,
        )

    turning_point = find_outer_turning_point(
        impact_parameter,
        metric.g_tt,
        metric.photon_sphere_radius,
        config.r_observer,
    )

    incoming = quad_real(
        lambda r: line_integrand(
            metric.g_tt(r),
            metric.g_rr(r),
            r,
            impact_parameter,
            outgoing=False,
        ),
        config.r_observer,
        turning_point,
        config=integration,
    )
    outgoing = quad_real(
        lambda r: line_integrand(
            metric.g_tt(r),
            metric.g_rr(r),
            r,
            impact_parameter,
            outgoing=True,
        ),
        turning_point,
        config.r_observer,
        config=integration,
    )
    return incoming + outgoing


def radial_intensity_profile(
    impact_parameters: np.ndarray,
    spacetime: JMN1Spacetime,
    config: RadiativeTransferConfig,
) -> np.ndarray:
    """Evaluate the circularly symmetric intensity profile `I_o(b)`."""

    values = [jmn1_intensity(float(b), spacetime, config) for b in impact_parameters]
    return np.asarray(values, dtype=float)


def schwarzschild_radial_intensity_profile(
    impact_parameters: np.ndarray,
    metric: SchwarzschildMetric,
    config: RadiativeTransferConfig,
) -> np.ndarray:
    """Evaluate the circularly symmetric Schwarzschild intensity profile `I_o(b)`."""

    values = [schwarzschild_intensity(float(b), metric, config) for b in impact_parameters]
    return np.asarray(values, dtype=float)
