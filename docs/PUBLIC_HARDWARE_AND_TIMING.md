# Hardware and timing appendix

## Public disclosure policy

The computations described in this report were performed with a closed-source MCDO solver build selected for public benchmarking.

Only the benchmarked build used for the reported tables is described. Internal solver versions, internal solver variants, internal implementation details, internal implementation details, and MCDO implementation details are not disclosed in this release.

The public package includes timing results, hardware metadata, graph certificates, validation summaries, and SHA256 manifests.

## Hardware

| component | value |
|---|---|
| CPU | Intel(R) Core(TM) i5-9500 CPU @ 3.00GHz |
| CPU cores | 6 |
| CPU logical processors | 6 |
| CPU max clock MHz | 3000 |
| RAM total GB | 15.88 |
| OS | Microsoft Windows 11 Pro 10.0.26200 build 26200, 64-bitowy |
| Disk C size GB | 237.5 |
| Disk C free GB | 100.94 |

## GPU present in system

| GPU | adapter RAM GB | driver |
|---|---:|---|
| NVIDIA GeForce RTX 3050 | 4 | 32.0.15.9174 |

GPU presence is reported as hardware metadata. GPU acceleration is not claimed unless a specific run explicitly reports GPU usage.

## Catalogue validation timings

| catalogue | case | count | valid | duplicate free | elapsed seconds | status |
|---|---|---:|---:|---:|---:|---|
| R39_35 | Ramsey(3,9,35) | 1 | True | True | not recorded | PASS_A_B |
| R37_22 | Ramsey(3,7,22) | 191 | True | True | not recorded | PASS_A_B |
| R46_35SOME | Ramsey(4,6,35) | 37 | True | True | not recorded | PASS_A_B |
| R45_24 | Ramsey(4,5,24) | 352366 | True | True | 153.6531138420105 | PASS_A_B_NODRAW |
| R38_27 | Ramsey(3,8,27) | 477142 | True | True | 630.0776364803314 | PASS_A_B_NODRAW |
| R37_21 | Ramsey(3,7,21) | 1118436 | True | True | 487.7384924888611 | PASS_A_B_NODRAW |
| R36_17 | Ramsey(3,6,17) | 7 | True | True | 32.69785952568054 | PASS_A_B_DRAW |
| R46_35SOME | Ramsey(4,6,35) | 37 | True | True | 205.15019416809082 | PASS_A_B_DRAW |
| R55_REFERENCE_SAMPLE | Ramsey(5,5,42) known reference sample | 656 | True | True | not recorded | PASS_R55_REFERENCE_SAMPLE_VALIDATED |

## Benchmark timing

| benchmark | mode | trials | mean speedup vs baseline | min speedup | max speedup | mean nodes |
|---|---|---:|---:|---:|---:|---:|
| Ramsey fragment benchmark A | baseline | 10 | 1.0 | 1.0 | 1.0 | 66598.3 |
| Ramsey fragment benchmark A | configuration_A | 10 | 1135.125191208084 | 1096.4666666666667 | 1169.421052631579 | 58.7 |
| Ramsey fragment benchmark A | configuration_B | 10 | 3.298211049038646 | 3.2621803114730676 | 3.33948432760364 | 20194.4 |
| Ramsey fragment benchmark A | selected_closed_source_configuration | 10 | 1922.345924885925 | 1817.054054054054 | 2019.909090909091 | 34.7 |
| R(4,5)_d12_R | selected_closed_source_configuration | 3 | 369.6276923076923 |  |  |  |
| R(3,8)_d7_B | selected_closed_source_configuration | 3 | 1254.5434681242336 |  |  |  |
| R(4,7)_d20_R | selected_closed_source_configuration | 3 | 1254.5402869749746 |  |  |  |
| R(3,8)_d6_B | selected_closed_source_configuration | 3 | 2.1123084916423407 |  |  |  |

## Public wording

The reported timings were obtained on the hardware listed above using the closed-source MCDO solver build selected for this report. The solver implementation is not released. The public evidence package contains validation outputs, timing tables, hardware metadata, graph certificates, and SHA256 manifests. Internal solver variants and private acceleration mechanisms are intentionally not disclosed in this release.


