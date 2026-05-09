# MDO Ramsey Master Publication Package

RUN_ID: MDO_RAMSEY_MASTER_PUBLICATION_20260509_092849

## Publication policy

This package publishes results, validation records, timing, hardware information and SHA256 evidence.

It does not publish the closed-source MCDO solver implementation, rule scoring, branch logic or internal method structure.

## Boundary statement

This package does not claim to solve open Ramsey numbers.

## Hardware profile

The hardware profile is stored in HARDWARE_PROFILE.json.

## Catalogue validation

| catalogue | case | type | count | expected | valid | duplicates ok | edge min | edge max | seconds | status |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| R39_35 | Ramsey(3,9,35) | official catalogue | 1 | 1 | True | True | 140 | 140 |  | PASS_A_B |
| R37_22 | Ramsey(3,7,22) | official catalogue | 191 | 191 | True | True | 60 | 66 |  | PASS_A_B |
| R46_35SOME | Ramsey(4,6,35) | official catalogue | 37 | 37 | True | True | 246 | 250 |  | PASS_A_B |
| R45_24 | Ramsey(4,5,24) | large official catalogue | 352366 | 352366 | True | True | 116 | 132 | 153.65 | PASS_A_B_NODRAW |
| R38_27 | Ramsey(3,8,27) | large official catalogue | 477142 | 477142 | True | True | 85 | 94 | 630.08 | PASS_A_B_NODRAW |
| R37_21 | Ramsey(3,7,21) | large official catalogue | 1118436 | 1118436 | True | True | 51 | 63 | 487.74 | PASS_A_B_NODRAW |
| R36_17 | Ramsey(3,6,17) | drawable small catalogue | 7 | 7 | True | True | 40 | 42 | 32.7 | PASS_A_B_DRAW |
| R46_35SOME | Ramsey(4,6,35) | drawable small catalogue | 37 | 37 | True | True | 246 | 250 | 205.15 | PASS_A_B_DRAW |
| R55_REFERENCE_SAMPLE | Ramsey(5,5,42) known reference sample | reference sample, not complete catalogue | 656 | 656 | True | True | 423 | 438 |  | PASS_R55_REFERENCE_SAMPLE_VALIDATED |

## Public benchmark timing

| benchmark | mode | trials | mean speedup | min speedup | max speedup | mean nodes |
|---|---|---:|---:|---:|---:|---:|
| V21 d13_R | baseline | 10 | 1.0 | 1.0 | 1.0 | 66598.3 |
| V21 d13_R | degree_only | 10 | 1135.125191208084 | 1096.4666666666667 | 1169.421052631579 | 58.7 |
| V21 d13_R | triangle_rule_only | 10 | 3.298211049038646 | 3.2621803114730676 | 3.33948432760364 | 20194.4 |
| V21 d13_R | full_mcdo | 10 | 1922.345924885925 | 1817.054054054054 | 2019.909090909091 | 34.7 |
| R(4,5)_d12_R | full_mcdo | 3 | 369.6276923076923 | None | None | None |
| R(3,8)_d7_B | full_mcdo | 3 | 1254.5434681242336 | None | None | None |
| R(4,7)_d20_R | full_mcdo | 3 | 1254.5402869749746 | None | None | None |
| R(3,8)_d6_B | full_mcdo | 3 | 2.1123084916423407 | None | None | None |

## Public claims ledger

| id | claim | status | disclosed | not disclosed |
|---|---|---|---|---|
| P1 | The project uses a closed-source MCDO solver and public certificate checks. | DISCLOSED | Results, validation outputs, timing, hardware, SHA256 manifests. | Solver implementation, rule scoring, branch-order logic, internal MCDO structure. |
| P2 | Official Ramsey catalogues are validated against McKay reference data. | SUPPORTED | Counts, validity flags, duplicate checks, edge statistics, SHA256. | Internal solver method. |
| P3 | MCDO produces repeatable acceleration on selected Ramsey fragments. | SUPPORTED | Timing and node-count benchmarks. | Exact mechanism producing the acceleration. |
| P4 | R(5,5) is not claimed solved. | BOUNDARY | Reference sample validation and hunter result. | No claim of complete search or proof. |

## Recommended public wording

The MCDO solver is closed-source in this release. Public artifacts include benchmark outputs, validation tables, timing results, hardware metadata and SHA256 manifests. The repository does not disclose the internal search strategy or rule-cut mechanism.

## Repository policy

Publish certificates, validation scripts, summary data and figures. Do not publish solver source code or method internals.
## Hardware and timing appendix

See PUBLIC_HARDWARE_AND_TIMING.md and PUBLIC_HARDWARE_PROFILE.json.

The reported timings were obtained using the closed-source MCDO solver build selected for this report. Internal solver variants, private search logic, branch scoring, rule selection, and implementation details are not disclosed.

