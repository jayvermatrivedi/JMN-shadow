# Mathematica Walkthrough

This file explains the original Mathematica workflow in plain language.

The original notebook has been renamed to:

- [jmn1_shadow_reproduction_m0p7_original.nb](../mathematica/jmn1_shadow_reproduction_m0p7_original.nb)

The filename now tells you exactly what it is:

- `jmn1`: the spacetime studied in the notebook
- `shadow_reproduction`: it reproduces shadow and intensity results
- `m0p7`: it uses `M0 = 0.7`
- `original`: this is the original source notebook, not the cleaned rewrite

## What The Notebook Does

The notebook is organized around one physical pipeline:

1. choose the JMN1 spacetime parameters
2. define the interior and exterior metric functions
3. define the null-geodesic radial momentum
4. define the redshift factors for infalling matter
5. build the intensity integrands
6. integrate intensity as a function of impact parameter `b`
7. convert the radial profile into a 2D image in the observer sky

## Step 1: Choose parameters

At the top of the notebook you see:

```mathematica
M0 = 0.7
rb = 2/M0
```

This means:

- the JMN1 parameter is fixed to `M0 = 0.7`
- the matching radius is `Rb = 2/M0 = 2.857142857...`
- the exterior Schwarzschild mass becomes `M_T = M0 Rb / 2 = 1`

That is exactly the parameter choice used for the JMN1 panels in Figure 2(c) and Figure 2(d).

## Step 2: Define the spacetime metric

The notebook defines:

- `Aint`
- `Bint`
- `Aext`
- `Bext`

These are the metric functions:

- `Aint`, `Bint` for the JMN1 interior
- `Aext`, `Bext` for the matched Schwarzschild exterior

So the metric is written as:

\[
ds^2 = -A(r)\,dt^2 + B(r)\,dr^2 + r^2 d\Omega^2
\]

with different formulas inside and outside the matching radius `rb`.

## Step 3: Define the radial null momentum

The notebook uses:

- `krtint`
- `krtext`

These are the radial components of the null geodesic momentum:

\[
k^r = \sqrt{\frac{g_{tt}}{g_{rr}}\left(1-\frac{g_{tt}b^2}{r^2}\right)}
\]

This is the core geodesic quantity needed for turning points and line-of-sight integration.

## Step 4: Define the redshift and blueshift factors

The notebook uses:

- `gintredshift`
- `greddhift`
- `gblueshift`

These represent:

- the redshift factor in the JMN1 interior
- the redshift branch in the exterior
- the blueshift branch in the exterior

Why are there two branches outside?

Because for rays with a turning point, the light ray has:

- an incoming branch before it reaches the minimum radius
- an outgoing branch after it turns around and travels to the observer

The notebook keeps those pieces separate so the line integral is physically correct.

## Step 5: Build the intensity integrands

The notebook defines:

- `IntredshiftJMN`
- `Intredshift`
- `Intblueshift`

These are the actual integrands used in the radiative transfer calculation.

They come from the paper's intensity formula

\[
I_o(X,Y)\propto -\int_\gamma \frac{g^3 k_t}{r^2 k^r}\,dr
\]

together with the emissivity prescription

\[
j(\nu_e)\propto \frac{\delta(\nu_e-\nu_*)}{r^2}.
\]

## Step 6: Build the intensity profile as a function of impact parameter

The notebook then creates tables such as:

- `data1`
- `data1re`
- `data2`
- `data2re`

These store intensity values for different impact parameters `b`.

### Schwarzschild branch

`data1` and `data1re` handle the outside-turning-point branch using the exterior Schwarzschild geometry.

### JMN1 branch

`data2` and `data2re` integrate:

- from `r = 0` to `r = rb` through the JMN1 interior
- from `r = rb` to `r = 50` through the Schwarzschild exterior

This is the intensity profile used for Figure 2(c).

## Step 7: Build the 2D observer image

The notebook defines:

- `Intensityobssch`
- `Intensityobsint`

These generate random points in the observer sky:

- choose a radius `b`
- choose an angle `t`
- convert to Cartesian coordinates `(X,Y)`
- evaluate the corresponding intensity

Then `ListDensityPlot` turns those samples into a 2D image.

### Which one is Figure 2(d)?

`Intensityobsint` is the JMN1 observer-sky image corresponding to Figure 2(d).

### Which one is Figure 2(b)?

`Intensityobssch` is the Schwarzschild observer-sky image corresponding to Figure 2(b).

## Why A Cleaned `.wl` File Was Added

The original `.nb` notebook is valuable as a source record, but it is hard to read because:

- variable names are short
- logic is spread across many cells
- there are no section-level explanations
- plotting cells and physics cells are mixed together

To make the project easier to understand, this repository also includes:

- [jmn1_shadow_reproduction_explained.wl](../mathematica/jmn1_shadow_reproduction_explained.wl)

That file rewrites the workflow into clearly commented sections.

## Recommended Order For A New User

1. Read the main [README.md](../README.md)
2. Read this walkthrough
3. Open the explained `.wl` file
4. Open the original notebook only after you know what each block is trying to do
