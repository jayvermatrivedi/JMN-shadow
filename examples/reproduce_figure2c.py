"""Reproduce the JMN1 intensity profile corresponding to Figure 2(c)."""

from __future__ import annotations

import os
import sys

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from src.intensity import RadiativeTransferConfig, radial_intensity_profile
from src.metric import JMN1Spacetime

matplotlib.use("Agg")


def main() -> None:
    spacetime = JMN1Spacetime(m0=0.7)
    rt_config = RadiativeTransferConfig(r_observer=50.0)

    b_positive = np.linspace(0.01, 15.0, 120)
    intensity_positive = radial_intensity_profile(b_positive, spacetime, rt_config)

    b_full = np.concatenate((-b_positive[::-1], b_positive))
    intensity_full = np.concatenate((intensity_positive[::-1], intensity_positive))

    fig, ax = plt.subplots(figsize=(7.0, 4.8), constrained_layout=True)
    ax.plot(b_full, intensity_full, color="black", lw=1.8)
    ax.axvline(spacetime.critical_impact_parameter, color="tab:red", ls="--", lw=1.0)
    ax.axvline(-spacetime.critical_impact_parameter, color="tab:red", ls="--", lw=1.0)
    ax.set_xlim(-15.0, 15.0)
    ax.set_xlabel(r"$b$")
    ax.set_ylabel(r"$I_{\rm o}(b)$")
    ax.set_title(r"JMN1 intensity profile for $M_0=0.7$ (paper Fig.~2(c))")
    ax.grid(alpha=0.2)

    output = os.path.join(PROJECT_ROOT, "figures", "figure2c_jmn1_profile.png")
    fig.savefig(output, dpi=300)
    print(output)


if __name__ == "__main__":
    main()
