(* ::Package:: *)

(* JMN1 shadow reproduction, explained version

   This file is a readable Mathematica companion to the original notebook:

     jmn1_shadow_reproduction_m0p7_original.nb

   Goal:
   - explain the meaning of each block
   - keep the same physical equations
   - provide a clearer top-to-bottom workflow

   Scope:
   - Schwarzschild figure 2(a), 2(b)
   - JMN1 figure 2(c), 2(d)
   - M0 = 0.7
*)


(* ================================================================ *)
(* 1. User parameters                                               *)
(* ================================================================ *)

ClearAll["Global`*"];

M0 = 0.7;
rb = 2/M0;

(* Because rb = 2/M0, the exterior Schwarzschild mass is 1. *)
MT = M0*rb/2;

rObserver = 50;
bCrit = 3*Sqrt[3]*MT;


(* ================================================================ *)
(* 2. Metric functions                                              *)
(* ================================================================ *)

(* JMN1 interior metric:
     ds^2 = -Aint dt^2 + Bint dr^2 + r^2 dOmega^2
*)
Aint[r_] := (1 - M0)*(r/rb)^(M0/(1 - M0));
Bint[r_] := 1/(1 - M0);

(* Exterior Schwarzschild metric with MT = 1:
     ds^2 = -Aext dt^2 + Bext dr^2 + r^2 dOmega^2
*)
Aext[r_] := 1 - (M0*rb/r);
Bext[r_] := 1/Aext[r];


(* ================================================================ *)
(* 3. Radial null momentum k^r                                      *)
(* ================================================================ *)

(* Paper Eq. (22) can be rewritten as

     k^r = Sqrt[(gtt/grr) (1 - gtt b^2/r^2)].

   The original notebook stores this separately for interior and exterior.
*)
krtint[r_, b_] := Sqrt[(Aint[r]/Bint[r])*(1 - (b^2*Aint[r]/r^2))];
krtext[r_, b_] := Sqrt[(Aext[r]/Bext[r])*(1 - (b^2*Aext[r]/r^2))];


(* ================================================================ *)
(* 4. Redshift factors for radially infalling matter                *)
(* ================================================================ *)

(* These formulas match the original notebook branches.
   The + sign is the outgoing branch after the turning point.
   The - sign is the incoming branch before the turning point.
*)
gintredshift[r_, b_] :=
  (
    (1/Aint[r]) +
    krtint[r, b]*(Bint[r]/Aint[r])*Sqrt[((1 - Aint[r])/(Aint[r]*Bint[r]))]
  )^(-1);

gredshift[r_, b_] :=
  (
    (1/Aext[r]) +
    krtext[r, b]*(Bext[r]/Aext[r])*Sqrt[((1 - Aext[r])/(Aext[r]*Bext[r]))]
  )^(-1);

gblueshift[r_, b_] :=
  (
    (1/Aext[r]) -
    krtext[r, b]*(Bext[r]/Aext[r])*Sqrt[((1 - Aext[r])/(Aext[r]*Bext[r]))]
  )^(-1);


(* ================================================================ *)
(* 5. Intensity integrands                                          *)
(* ================================================================ *)

(* These are the line-of-sight integrands used for Eq. (32). *)
IntredshiftJMN[r_, b_] := (gintredshift[r, b]^3)*(Aint[r]/r^2)*(1/krtint[r, b]);
Intredshift[r_, b_] := (gredshift[r, b]^3)*(Aext[r]/r^2)*(1/krtext[r, b]);
Intblueshift[r_, b_] := -(gblueshift[r, b]^3)*(Aext[r]/r^2)*(1/krtext[r, b]);


(* ================================================================ *)
(* 6. Turning point for Schwarzschild exterior                      *)
(* ================================================================ *)

(* The turning point solves:

     r / Sqrt[Aext[r]] == b

   We use the outer solution, the one relevant for rays coming from infinity.
*)
turningPoint[b_?NumericQ] := Module[{roots},
  roots = Select[r /. NSolve[r/Sqrt[Aext[r]] == b, r, Reals], # > 3*MT &];
  First[roots]
];


(* ================================================================ *)
(* 7. Observed intensity profiles I_o(b)                            *)
(* ================================================================ *)

(* Schwarzschild profile: figure 2(a) *)
schwarzschildIntensity[b_?NumericQ] := Module[{rtp},
  If[b < bCrit,
    Re@NIntegrate[Intredshift[r, b], {r, 2.000001, rObserver}],
    rtp = turningPoint[b];
    Re@(
      NIntegrate[Intblueshift[r, b], {r, rObserver, rtp}] +
      NIntegrate[Intredshift[r, b], {r, rtp, rObserver}]
    )
  ]
];

(* JMN1 profile: figure 2(c) *)
jmn1Intensity[b_?NumericQ] := Module[{rtp},
  If[b < bCrit,
    Re@(
      NIntegrate[IntredshiftJMN[r, b], {r, 0.000001, rb}] +
      NIntegrate[Intredshift[r, b], {r, rb, rObserver}]
    ),
    rtp = turningPoint[b];
    Re@(
      NIntegrate[Intblueshift[r, b], {r, rObserver, rtp}] +
      NIntegrate[Intredshift[r, b], {r, rtp, rObserver}]
    )
  ]
];


(* ================================================================ *)
(* 8. Sample intensity profiles for plotting                        *)
(* ================================================================ *)

schwarzschildProfileData[] := Module[{bValues, intensities},
  bValues = Range[0.01, 15, 0.125];
  intensities = schwarzschildIntensity /@ bValues;
  Join[
    Transpose[{-Reverse[bValues], Reverse[intensities]}],
    Transpose[{bValues, intensities}]
  ]
];

jmn1ProfileData[] := Module[{bValues, intensities},
  bValues = Range[0.01, 15, 0.125];
  intensities = jmn1Intensity /@ bValues;
  Join[
    Transpose[{-Reverse[bValues], Reverse[intensities]}],
    Transpose[{bValues, intensities}]
  ]
];


(* ================================================================ *)
(* 9. Figure 2(a) and 2(c): intensity profile plots                 *)
(* ================================================================ *)

makeFigure2a[] := ListLinePlot[
  schwarzschildProfileData[],
  Frame -> True,
  FrameLabel -> {"b", "I_o(b)"},
  PlotLabel -> "Figure 2(a): Schwarzschild intensity profile",
  PlotStyle -> Black,
  ImageSize -> Large
];

makeFigure2c[] := ListLinePlot[
  jmn1ProfileData[],
  Frame -> True,
  FrameLabel -> {"b", "I_o(b)"},
  PlotLabel -> "Figure 2(c): JMN1 intensity profile, M0 = 0.7",
  PlotStyle -> Black,
  ImageSize -> Large
];


(* ================================================================ *)
(* 10. Circular image from radial intensity                         *)
(* ================================================================ *)

(* Because the spacetime is spherically symmetric, the image only
   depends on b = Sqrt[X^2 + Y^2].
*)
buildCircularImage[intensityFunction_, bMax_: 10, n_: 250] := Module[
  {xs, ys, grid},
  xs = Subdivide[-bMax, bMax, n];
  ys = Subdivide[-bMax, bMax, n];
  grid = Table[
    intensityFunction[Sqrt[x^2 + y^2]],
    {y, ys}, {x, xs}
  ];
  {xs, ys, grid}
];


(* ================================================================ *)
(* 11. Figure 2(b) and 2(d): shadow images                          *)
(* ================================================================ *)

makeFigure2b[] := Module[{img},
  img = buildCircularImage[schwarzschildIntensity, 10, 180];
  ListDensityPlot[
    Flatten[
      Table[
        {img[[1, ix]], img[[2, iy]], img[[3, iy, ix]]},
        {iy, Length[img[[2]]]}, {ix, Length[img[[1]]]}
      ],
      1
    ],
    PlotRange -> {{-10, 10}, {-10, 10}},
    ColorFunction -> "SunsetColors",
    Frame -> True,
    FrameLabel -> {"X", "Y"},
    PlotLabel -> "Figure 2(b): Schwarzschild shadow image",
    ImageSize -> Large
  ]
];

makeFigure2d[] := Module[{img},
  img = buildCircularImage[jmn1Intensity, 10, 180];
  ListDensityPlot[
    Flatten[
      Table[
        {img[[1, ix]], img[[2, iy]], img[[3, iy, ix]]},
        {iy, Length[img[[2]]]}, {ix, Length[img[[1]]]}
      ],
      1
    ],
    PlotRange -> {{-10, 10}, {-10, 10}},
    ColorFunction -> "SunsetColors",
    Frame -> True,
    FrameLabel -> {"X", "Y"},
    PlotLabel -> "Figure 2(d): JMN1 shadow image, M0 = 0.7",
    ImageSize -> Large
  ]
];


(* ================================================================ *)
(* 12. How to use this file                                         *)
(* ================================================================ *)

(* Evaluate this file, then run:

     makeFigure2a[]
     makeFigure2b[]
     makeFigure2c[]
     makeFigure2d[]

   This explained file is designed to be read top-to-bottom.
*)
