# JMN Shadow Reproduction Toolkit

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/jayvermatrivedi/JMN-shadow/blob/main/notebooks/JMN_Shadow_Google_Colab.ipynb)

Beginner-friendly reproduction code for the paper *Shadow of a naked singularity without photon sphere* by Ashok B. Joshi, Dipanjan Dey, Pankaj S. Joshi, and Parth Bambhaniya, Phys. Rev. D **102**, 024022 (2020), DOI: `10.1103/PhysRevD.102.024022`.

This repository is designed so a first-time user can:

- run the figures in Google Colab without local setup
- reproduce the Schwarzschild and JMN1 shadow plots in Python
- inspect a renamed copy of the original Mathematica notebook
- read a step-by-step Mathematica explanation before opening the notebook

## Quick Links

- Run online in Colab:
  `https://colab.research.google.com/github/jayvermatrivedi/JMN-shadow/blob/main/notebooks/JMN_Shadow_Google_Colab.ipynb`
- Python one-command runner:
  [examples/run_all_figures.py](examples/run_all_figures.py)
- Original notebook, renamed clearly:
  [mathematica/jmn1_shadow_reproduction_m0p7_original.nb](mathematica/jmn1_shadow_reproduction_m0p7_original.nb)
- Explained Mathematica script:
  [mathematica/jmn1_shadow_reproduction_explained.wl](mathematica/jmn1_shadow_reproduction_explained.wl)
- Mathematica walkthrough:
  [docs/MATHEMATICA_WALKTHROUGH.md](docs/MATHEMATICA_WALKTHROUGH.md)

The repository currently supports:

- Figure 2(a): Schwarzschild intensity profile
- Figure 2(b): Schwarzschild shadow image
- Figure 2(c): JMN1 intensity profile with `M0 = 0.7`
- Figure 2(d): JMN1 shadow image with `M0 = 0.7`

It does **not** currently implement the second naked-singularity model from the paper.

## Start Here

If you are new to GitHub or scientific code, use one of these three paths:

### Option 1: Easiest, use Google Colab

1. Open the notebook:
   [notebooks/JMN_Shadow_Google_Colab.ipynb](notebooks/JMN_Shadow_Google_Colab.ipynb)
2. Upload that notebook to Google Colab, or copy its cells into a new Colab notebook.
3. Run the cells from top to bottom.

This requires no local Python installation.

### Option 2: Run locally with Python

If you already have Python installed:

```bash
git clone https://github.com/jayvermatrivedi/JMN-shadow.git
cd JMN-shadow
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python examples/run_all_figures.py
```

If you are on Windows PowerShell, use:

```powershell
.venv\Scripts\Activate.ps1
```

This will generate all four supported figures in the `figures/` folder.

### Option 3: Read or run the Mathematica version

Open these files:

- Original notebook, renamed for clarity:
  [mathematica/jmn1_shadow_reproduction_m0p7_original.nb](mathematica/jmn1_shadow_reproduction_m0p7_original.nb)
- Explained Mathematica script:
  [mathematica/jmn1_shadow_reproduction_explained.wl](mathematica/jmn1_shadow_reproduction_explained.wl)
- Mathematica walkthrough:
  [docs/MATHEMATICA_WALKTHROUGH.md](docs/MATHEMATICA_WALKTHROUGH.md)

If you only want to understand what the Mathematica code is doing, start with the walkthrough file.

## Repository Layout

```text
JMN-shadow/
|
|-- README.md
|-- requirements.txt
|-- LICENSE
|
|-- src/
|   |-- metric.py
|   |-- geodesics.py
|   |-- intensity.py
|   |-- shadow.py
|   |-- raytracing.py
|   `-- utils.py
|
|-- examples/
|   |-- reproduce_figure2a.py
|   |-- reproduce_figure2b.py
|   |-- reproduce_figure2c.py
|   |-- reproduce_figure2d.py
|   `-- run_all_figures.py
|
|-- figures/
|   `-- output images are saved here
|
|-- notebooks/
|   `-- JMN_Shadow_Google_Colab.ipynb
|
|-- mathematica/
|   |-- jmn1_shadow_reproduction_m0p7_original.nb
|   `-- jmn1_shadow_reproduction_explained.wl
|
|-- docs/
|   `-- MATHEMATICA_WALKTHROUGH.md
|
`-- reference/
    `-- joshi_2020_shadow_of_a_naked_singularity_without_photon_sphere.pdf
```

## What Each Python File Does

### [src/metric.py](src/metric.py)

Defines the spacetime metric functions:

- Schwarzschild metric
- JMN1 interior metric
- JMN1 exterior Schwarzschild matching

### [src/geodesics.py](src/geodesics.py)

Implements:

- effective potential
- turning-point impact parameter
- radial null momentum
- redshift factor for infalling emitters

### [src/intensity.py](src/intensity.py)

Implements the radiative transfer prescription from the paper:

- emissivity
- branchwise redshift/blueshift intensity integrands
- observed intensity profile `I_o(b)` for Schwarzschild and JMN1

### [src/shadow.py](src/shadow.py)

Defines the circular shadow boundaries:

- Schwarzschild shadow radius `3 sqrt(3) M`
- JMN1 shadow radius inherited from the exterior Schwarzschild photon sphere

### [src/raytracing.py](src/raytracing.py)

Builds the 2D observer-sky image from the 1D radial intensity profile.

## Exact Commands To Run

### Local Python: generate all figures

```bash
python examples/run_all_figures.py
```

Expected output files:

- `figures/figure2a_schwarzschild_profile.png`
- `figures/figure2b_schwarzschild_shadow.png`
- `figures/figure2c_jmn1_profile.png`
- `figures/figure2d_jmn1_shadow.png`

### Local Python: generate only one figure

Schwarzschild intensity profile:

```bash
python examples/reproduce_figure2a.py
```

Schwarzschild shadow image:

```bash
python examples/reproduce_figure2b.py
```

JMN1 intensity profile:

```bash
python examples/reproduce_figure2c.py
```

JMN1 shadow image:

```bash
python examples/reproduce_figure2d.py
```

## Google Colab Instructions

If you have never used Colab before, follow these exact steps:

1. Go to `https://colab.research.google.com`
2. Create a new notebook
3. Open this repository notebook:
   [notebooks/JMN_Shadow_Google_Colab.ipynb](notebooks/JMN_Shadow_Google_Colab.ipynb)
4. Copy the cells into Colab, or upload the notebook file
5. Run each cell from top to bottom

The Colab notebook will:

1. clone the GitHub repository
2. install the required packages
3. generate the four supported figures
4. display them inside the notebook

## Mathematica Instructions

If you want the original project source:

- open [mathematica/jmn1_shadow_reproduction_m0p7_original.nb](mathematica/jmn1_shadow_reproduction_m0p7_original.nb)

If you want a readable version:

- open [mathematica/jmn1_shadow_reproduction_explained.wl](mathematica/jmn1_shadow_reproduction_explained.wl)

If you want a plain-English explanation of each block:

- read [docs/MATHEMATICA_WALKTHROUGH.md](docs/MATHEMATICA_WALKTHROUGH.md)

## Physics Summary

This repository reproduces the shadow calculation for a spherically symmetric, optically thin accretion flow in two spacetimes:

- Schwarzschild black hole
- JMN1 naked singularity spacetime matched to a Schwarzschild exterior

The key ideas are:

- light rays are traced using null geodesics
- the turning point is determined by the impact parameter
- the observed intensity is computed by integrating the emissivity along the ray
- the shadow is the dark central region in the observer sky

### JMN1 metric used here

The JMN1 interior metric is

\[
ds^2 = -A_{\rm int}(r)\,dt^2 + B_{\rm int}(r)\,dr^2 + r^2 d\Omega^2
\]

with

\[
A_{\rm int}(r) = (1-M_0)\left(\frac{r}{R_b}\right)^{\frac{M_0}{1-M_0}},
\qquad
B_{\rm int}(r)=\frac{1}{1-M_0}.
\]

The exterior is Schwarzschild with

\[
A_{\rm ext}(r)=1-\frac{M_0 R_b}{r},
\qquad
B_{\rm ext}(r)=\left(1-\frac{M_0 R_b}{r}\right)^{-1}.
\]

For the repository default case:

- `M0 = 0.7`
- `Rb = 2 / M0`
- `M_T = M0 Rb / 2 = 1`

### Main observables

- Schwarzschild photon-sphere shadow radius:
  \[
  b_{\rm ph}=3\sqrt{3}M
  \]
- JMN1 shadow radius in the supported case:
  \[
  b_{\rm ph}=3\sqrt{3}M_T
  \]

## Figure Mapping

### Supported now

- Figure 2(a): Schwarzschild intensity profile
- Figure 2(b): Schwarzschild shadow image
- Figure 2(c): JMN1 intensity profile with `M0 = 0.7`
- Figure 2(d): JMN1 shadow image with `M0 = 0.7`

### Not included yet

- Figure 2(e)
- Figure 2(f)

Those correspond to the second naked-singularity spacetime and are intentionally excluded from the current Python implementation.

## Common Problems

### `python: command not found`

Use `python3` instead of `python`.

### `ModuleNotFoundError`

You probably did not install dependencies. Run:

```bash
pip install -r requirements.txt
```

### Figures are not appearing on screen

The scripts save figures to the `figures/` folder. Open the PNG files there.

### I only want the final outputs

Run:

```bash
python examples/run_all_figures.py
```

Then open the files in `figures/`.

## Citation

If you use this repository, cite the original paper:

```bibtex
@article{Joshi:2020tlq,
  author = {Joshi, Ashok B. and Dey, Dipanjan and Joshi, Pankaj S. and Bambhaniya, Parth},
  title = {Shadow of a naked singularity without photon sphere},
  journal = {Physical Review D},
  volume = {102},
  number = {2},
  pages = {024022},
  year = {2020},
  doi = {10.1103/PhysRevD.102.024022}
}
```
