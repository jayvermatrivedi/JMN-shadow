# JMN Shadow and Ray Tracing in Mathematica and Python

This repository ports a Mathematica implementation of null geodesics, shadow formation, and radiative transfer in the Schwarzschild and Joshi-Malafarina-Narayan (JMN1) spacetimes to a modular Python codebase. The reference paper in this folder is:

- Ashok B. Joshi, Dipanjan Dey, Pankaj S. Joshi, and Parth Bambhaniya, *Shadow of a naked singularity without photon sphere*, Phys. Rev. D **102**, 024022 (2020), DOI: `10.1103/PhysRevD.102.024022`.

The Python examples reproduce the Schwarzschild plots corresponding to Figure 2(a) and Figure 2(b), and the JMN1 plots corresponding to Figure 2(c) and Figure 2(d), of that paper.

## Scientific Motivation

The central question is whether compact objects with naked singularities can produce observational signatures that differ from black holes. In the paper, the authors compare:

- Schwarzschild black holes
- JMN1 naked singularities
- a second asymptotically flat naked singularity without a photon sphere

This Python repository currently implements the Schwarzschild and JMN1 cases only. The second naked-singularity model from the paper is intentionally left out.

The observable is the intensity pattern on the observer sky produced by light emitted from an optically thin, spherically symmetric, freely infalling accretion flow. The shadow is the dark central region associated with geodesics that cannot connect the bright background to the observer in the usual way.

## Physics Summary

### 1. JMN1 metric used in the code

The Mathematica notebook uses the JMN1 interior metric in the form

\[
ds^2 = -A_{\rm int}(r)\,dt^2 + B_{\rm int}(r)\,dr^2 + r^2 d\Omega^2,
\]

with

\[
A_{\rm int}(r) = (1-M_0)\left(\frac{r}{R_b}\right)^{\frac{M_0}{1-M_0}},
\qquad
B_{\rm int}(r) = \frac{1}{1-M_0}.
\]

This is paper Eq. (19). In the notebook:

- `M0 = 0.7`
- `rb = 2/M0 = 2.857142857...`

The JMN1 interior is matched to an exterior Schwarzschild region at `r = R_b`, with

\[
A_{\rm ext}(r)=1-\frac{M_0 R_b}{r},
\qquad
B_{\rm ext}(r)=\left(1-\frac{M_0 R_b}{r}\right)^{-1}.
\]

Because the notebook sets `R_b = 2/M0`, the exterior mass is

\[
M_T = \frac{M_0 R_b}{2}=1,
\]

so the exterior metric reduces numerically to Schwarzschild with

\[
A_{\rm ext}(r)=1-\frac{2}{r}, \qquad B_{\rm ext}(r)=\left(1-\frac{2}{r}\right)^{-1}.
\]

### 1b. Schwarzschild metric used in the code

For the Schwarzschild reference case, the code uses

\[
ds^2 = -\left(1-\frac{2M}{r}\right)dt^2
\;+\; \left(1-\frac{2M}{r}\right)^{-1}dr^2
\;+\; r^2 d\Omega^2,
\]

with `M = 1` for the Figure 2(a)/(b) reproduction.

### 2. Meaning of the parameters

- `M0`: dimensionless JMN1 parameter, with `0 < M0 < 1`
- `Rb` or `rb`: matching radius between the JMN1 interior and exterior Schwarzschild geometry
- `M_T`: Schwarzschild mass of the exterior region
- `b = h/\gamma`: impact parameter of the photon
- `r_tp`: turning-point radius
- `r_ph`: photon-sphere radius

For the notebook and for Figure 2(c)/(d):

- `M0 = 0.7`
- `Rb = 2.857142857...`
- `M_T = 1`
- `r_ph = 3`
- `b_ph = 3\sqrt{3} = 5.1961524227...`

For the Schwarzschild case used in Figure 2(a)/(b):

- `M = 1`
- `r_h = 2`
- `r_ph = 3`
- `b_ph = 3\sqrt{3} = 5.1961524227...`

### 3. Null geodesics and effective potential

The paper uses the general static, spherically symmetric metric

\[
ds^2 = -g_{tt}(r)\,dt^2 + g_{rr}(r)\,dr^2 + r^2 d\Omega^2,
\]

and in the equatorial plane the null geodesics satisfy paper Eq. (22):

\[
g_{tt}g_{rr}\left(\frac{dr}{d\lambda}\right)^2 = \frac{1}{b^2} - V_{\rm eff}(r),
\qquad
V_{\rm eff}(r)=\frac{g_{tt}(r)}{r^2}.
\]

The notebook implements the radial momentum magnitude as

\[
k^r = \sqrt{\frac{g_{tt}}{g_{rr}}\left(1-\frac{g_{tt}b^2}{r^2}\right)},
\]

through the definitions:

- `krtint` for the JMN1 interior
- `krtext` for the Schwarzschild exterior

These are the exact algebraic expressions used in `src/geodesics.py`.

### 4. Impact parameters and photon sphere

At a turning point, paper Eq. (23) gives

\[
b_{\rm tp} = \frac{r_{\rm tp}}{\sqrt{g_{tt}(r_{\rm tp})}}.
\]

For the exterior Schwarzschild region with `M_T = 1`,

\[
r_{\rm ph}=3, \qquad b_{\rm ph}=3\sqrt{3}.
\]

Since the notebook works with `M0 = 0.7 > 2/3`, the JMN1 spacetime has an effective photon sphere in the exterior Schwarzschild region. That is exactly why the notebook starts the exterior turning-point branch at

- `5.196152422706632`

which is `3 sqrt(3)`, the critical impact parameter.

### 5. Redshift factor and infalling matter

The paper assumes a spherically symmetric, radially freely falling emitter. Its four-velocity is paper Eq. (29):

\[
u^t_e = \frac{1}{g_{tt}},
\qquad
u^r_e = -\sqrt{\frac{1-g_{tt}}{g_{tt}g_{rr}}},
\qquad
u^\theta_e=u^\phi_e=0.
\]

The observed redshift factor is paper Eqs. (30)-(31):

\[
g = \frac{\nu_o}{\nu_e}
=
\left[
\frac{1}{g_{tt}}
\pm
k^r\frac{g_{rr}}{g_{tt}}
\sqrt{\frac{1-g_{tt}}{g_{tt}g_{rr}}}
\right]^{-1},
\]

with the `+` branch corresponding to the outgoing part of the ray after the turning point and the `-` branch to the incoming part before the turning point. In the notebook these are:

- `gintredshift`
- `greddhift` (typo in notebook name, but this is the exterior redshift branch)
- `gblueshift`

### 6. Emissivity and observed intensity

The emissivity prescription in the paper is

\[
j(\nu_e) \propto \frac{\delta(\nu_e-\nu_*)}{r^2},
\]

which is paper Eq. (26). After integrating over observed frequency, paper Eq. (32) gives

\[
I_o(X,Y)\propto -\int_\gamma \frac{g^3 k_t}{r^2 k^r}\,dr,
\qquad X^2+Y^2=b^2.
\]

The Mathematica notebook rewrites this in branch form as:

- `IntredshiftJMN := (gintredshift^3) * (Aint/r^2) * (1/krtint)`
- `Intredshift    := (greddhift^3)  * (Aext/r^2) * (1/krtext)`
- `Intblueshift   := -(gblueshift^3) * (Aext/r^2) * (1/krtext)`

Those expressions are implemented directly in `src/intensity.py`.

### 7. Ray-tracing and image construction

Because the model is spherically symmetric, the observer image depends only on

\[
b=\sqrt{X^2+Y^2}.
\]

The notebook computes the intensity profile first as a function of `b`, then samples random polar coordinates `(b, \theta)` in the observer plane and evaluates the line-of-sight integrals there before using `ListDensityPlot`. The Python port keeps the same physics but builds a deterministic circular image from the radial profile, which is numerically cleaner and easier to reproduce.

## Mathematica Notebook to Paper Cross-Reference

### Metric sector

- Notebook `Aint`, `Bint`: paper Eq. (19), JMN1 interior
- Notebook `Aext`, `Bext`: Schwarzschild exterior matched to JMN1

### Geodesics

- Notebook `krtint`, `krtext`: paper Eq. (22) rewritten as the radial momentum magnitude
- Turning-point condition solved by `NSolve[r / Sqrt[Aext] == b, r]`: paper Eq. (23)

### Radiative transfer

- Notebook `gintredshift`, `greddhift`, `gblueshift`: paper Eqs. (29)-(31)
- Notebook `IntredshiftJMN`, `Intredshift`, `Intblueshift`: paper Eq. (32) with the emissivity from Eq. (26)

### Figure 2(a) and Figure 2(b)

The notebook also builds the Schwarzschild panels using the pure exterior branch:

- `data1`
- `data1re`
- the corresponding random observer-sky sampling in `Intensityobssch`

These are the paper's Schwarzschild intensity profile and shadow image, Figure 2(a) and Figure 2(b).

### Figure 2(c)

The notebook constructs the JMN1 intensity profile using:

- `data2`
- `data2re`
- `Dataeff1 = Join[data2, data1]`
- `Dataeff2 = Join[data2re, data1re]`
- `ListLinePlot[{Dataeff1, Dataeff2}, ...]`

The JMN1 part itself is `data2` and `data2re`, which integrate:

- `IntredshiftJMN` from `r = 0` to `r = rb`
- `Intredshift` from `r = rb` to `r = 50`

for `0.001 <= b <= 3 sqrt(3)`.

This corresponds to the middle-left panel of the paper, Figure 2(c), for `M0 = 0.7`.

### Figure 2(d)

The notebook constructs the JMN1 observer-sky image with:

- `Intensityobsint`
- `ListDensityPlot[{Intensityobssch, Intensityobsint}, ...]`

The JMN1-specific image is `Intensityobsint`, which randomly samples `(X,Y)` through polar coordinates and evaluates the same JMN1 line-of-sight integrals. This is the middle-right panel of the paper, Figure 2(d), again with `M0 = 0.7`.

## Python Code Structure

```text
src/
  metric.py       Metric definitions and JMN1 matching relations
  geodesics.py    Effective potential, radial null momentum, redshift
  shadow.py       Shadow radii and circular boundaries
  intensity.py    Emissivity and observed intensity integrals
  raytracing.py   Circular observer-sky image construction
  utils.py        Quadrature and root-finding helpers

examples/
  reproduce_figure2a.py
  reproduce_figure2b.py
  reproduce_figure2c.py
  reproduce_figure2d.py
```

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

Reproduce the Schwarzschild intensity profile of Figure 2(a):

```bash
python examples/reproduce_figure2a.py
```

Reproduce the Schwarzschild observer-sky image of Figure 2(b):

```bash
python examples/reproduce_figure2b.py
```

Reproduce the JMN1 intensity profile of Figure 2(c):

```bash
python examples/reproduce_figure2c.py
```

Reproduce the JMN1 observer-sky image of Figure 2(d):

```bash
python examples/reproduce_figure2d.py
```

Outputs are written to:

- `figures/figure2a_schwarzschild_profile.png`
- `figures/figure2b_schwarzschild_shadow.png`
- `figures/figure2c_jmn1_profile.png`
- `figures/figure2d_jmn1_shadow.png`

## Numerical Method

- One-dimensional line-of-sight integrals are evaluated with `scipy.integrate.quad`.
- Exterior turning points for `b > 3 sqrt(3)` are found by solving
  \[
  \frac{r}{\sqrt{g_{tt}(r)}} = b
  \]
  with a root outside the photon sphere, using `scipy.optimize.brentq`.
- The 2D image is reconstructed from the radial intensity profile using interpolation on a Cartesian observer grid.

## Reproducing Figure 2(a) to Figure 2(d)

For the Schwarzschild case use:

- `M = 1`

For the JMN1 case use:

- `M0 = 0.7`
- `Rb = 2/M0`
- `M_T = 1`

These are exactly the values used in the provided Mathematica notebook and the paper caption for the Schwarzschild and JMN1 panels of Figure 2.

## Original Mathematica Workflow

The notebook flow is:

1. Set `M0` and `rb`
2. Define the JMN1 interior and exterior metric functions
3. Build `k^r` for interior and exterior null geodesics
4. Build redshift and blueshift factors for the infalling emitter
5. Form the branch-wise intensity integrands
6. Integrate over radius for selected impact parameters
7. Assemble the intensity-vs-`b` curves
8. Sample the observer plane and produce the final density plot

The Python port mirrors that sequence, but separates each physical step into a dedicated module.

## References

1. A. B. Joshi, D. Dey, P. S. Joshi, and P. Bambhaniya, *Shadow of a naked singularity without photon sphere*, Phys. Rev. D **102**, 024022 (2020).
2. P. S. Joshi, D. Malafarina, and R. Narayan, works on JMN naked singularity spacetimes cited in the paper.

## Citation

If you use this code, cite the paper whose Mathematica implementation is ported here, and note explicitly that the reproduced Schwarzschild and JMN1 images correspond to Figure 2(a)-2(d):

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
