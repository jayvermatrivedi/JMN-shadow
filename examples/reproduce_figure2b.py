"""Reproduce the Schwarzschild observer-sky image corresponding to Figure 2(b)."""

from __future__ import annotations

import os
import sys

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.patches import Circle

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from src.intensity import RadiativeTransferConfig
from src.metric import SchwarzschildMetric
from src.raytracing import ImageConfig, build_schwarzschild_image
from src.shadow import schwarzschild_shadow


def main() -> None:
    metric = SchwarzschildMetric(mass=1.0)
    rt_config = RadiativeTransferConfig(r_observer=50.0)
    image_config = ImageConfig(field_of_view=10.0, pixels=400, b_max_profile=15.0, profile_samples=120)

    x_axis, y_axis, image = build_schwarzschild_image(metric, rt_config, image_config)
    shadow = schwarzschild_shadow(metric)

    fig, ax = plt.subplots(figsize=(6.5, 6.2), constrained_layout=True)
    im = ax.imshow(
        image,
        extent=(x_axis[0], x_axis[-1], y_axis[0], y_axis[-1]),
        origin="lower",
        cmap="cividis",
        interpolation="bicubic",
    )
    ax.add_patch(Circle((0.0, 0.0), shadow.radius, edgecolor="white", facecolor="none", lw=1.2, ls="--"))
    ax.set_xlabel(r"$X$")
    ax.set_ylabel(r"$Y$")
    ax.set_title(r"Schwarzschild observer-sky image for $M=1$ (paper Fig.~2(b))")
    cbar = fig.colorbar(im, ax=ax, shrink=0.88)
    cbar.set_label(r"$I_{\rm o}(X,Y)$")

    output = os.path.join(PROJECT_ROOT, "figures", "figure2b_schwarzschild_shadow.png")
    fig.savefig(output, dpi=300)
    print(output)


if __name__ == "__main__":
    main()
