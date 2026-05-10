"""Observer-sky image construction for circularly symmetric shadows."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.interpolate import interp1d

from .intensity import (
    RadiativeTransferConfig,
    radial_intensity_profile,
    schwarzschild_radial_intensity_profile,
)
from .metric import JMN1Spacetime, SchwarzschildMetric


@dataclass(frozen=True)
class ImageConfig:
    """Sampling configuration for the observer-sky image."""

    field_of_view: float = 10.0
    pixels: int = 500
    b_max_profile: float = 15.0
    profile_samples: int = 200


def build_jmn1_image(
    spacetime: JMN1Spacetime,
    rt_config: RadiativeTransferConfig,
    image_config: ImageConfig,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Construct the circular observer-sky image from the radial intensity profile."""

    b_samples = np.linspace(0.01, image_config.b_max_profile, image_config.profile_samples)
    profile = radial_intensity_profile(b_samples, spacetime, rt_config)
    interpolator = interp1d(
        b_samples,
        profile,
        kind="linear",
        bounds_error=False,
        fill_value=(profile[0], profile[-1]),
    )

    extent = image_config.field_of_view
    axis = np.linspace(-extent, extent, image_config.pixels)
    x_grid, y_grid = np.meshgrid(axis, axis, indexing="xy")
    b_grid = np.sqrt(x_grid**2 + y_grid**2)
    image = interpolator(np.clip(b_grid, b_samples[0], b_samples[-1]))
    return axis, axis, image


def build_schwarzschild_image(
    metric: SchwarzschildMetric,
    rt_config: RadiativeTransferConfig,
    image_config: ImageConfig,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Construct the circular Schwarzschild observer-sky image."""

    b_samples = np.linspace(0.01, image_config.b_max_profile, image_config.profile_samples)
    profile = schwarzschild_radial_intensity_profile(b_samples, metric, rt_config)
    interpolator = interp1d(
        b_samples,
        profile,
        kind="linear",
        bounds_error=False,
        fill_value=(profile[0], profile[-1]),
    )

    extent = image_config.field_of_view
    axis = np.linspace(-extent, extent, image_config.pixels)
    x_grid, y_grid = np.meshgrid(axis, axis, indexing="xy")
    b_grid = np.sqrt(x_grid**2 + y_grid**2)
    image = interpolator(np.clip(b_grid, b_samples[0], b_samples[-1]))
    return axis, axis, image
