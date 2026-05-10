"""Null-geodesic relations used in the paper and notebook."""

from __future__ import annotations

import numpy as np

from .utils import safe_sqrt


def effective_potential(g_tt: float, r: float) -> float:
    """Paper Eq. (22): `V_eff = g_tt / r^2`."""
    return g_tt / (r * r)


def impact_parameter_at_turning_point(g_tt: float, r: float) -> float:
    """Paper Eq. (23): `b_tp = r_tp / sqrt(g_tt(r_tp))`."""
    return r / np.sqrt(g_tt)


def radial_null_momentum(g_tt: float, g_rr: float, r: float, impact_parameter: float) -> float:
    """Return the radial null momentum magnitude `k^r`.

    The notebook definitions `krtint` and `krtext` implement

        k^r = sqrt((g_tt / g_rr) * (1 - g_tt b^2 / r^2)).
    """

    radicand = (g_tt / g_rr) * (1.0 - g_tt * impact_parameter * impact_parameter / (r * r))
    return safe_sqrt(radicand)


def free_fall_four_velocity(g_tt: float, g_rr: float) -> tuple[float, float]:
    """Paper Eq. (29) for a radially free-falling emitter."""
    u_t = 1.0 / g_tt
    u_r = -safe_sqrt((1.0 - g_tt) / (g_tt * g_rr))
    return u_t, u_r


def redshift_factor(g_tt: float, g_rr: float, r: float, impact_parameter: float, *, outgoing: bool) -> float:
    """Paper Eqs. (30)-(31) for the observed redshift factor `g = nu_o / nu_e`.

    `outgoing=True` corresponds to the redshift branch after the turning point.
    `outgoing=False` corresponds to the blueshift branch before the turning point.
    """

    kr = radial_null_momentum(g_tt, g_rr, r, impact_parameter)
    sign = 1.0 if outgoing else -1.0
    denominator = (1.0 / g_tt) + sign * kr * (g_rr / g_tt) * safe_sqrt((1.0 - g_tt) / (g_tt * g_rr))
    return 1.0 / denominator
