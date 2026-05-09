# MDO Ramsey Benchmarks

Public benchmark and validation artifacts for a closed-source MDO/MCDO Ramsey graph solver.

## Scope

This repository publishes:

- benchmark results
- timing tables
- hardware metadata
- official catalogue validation summaries
- graph certificate summaries
- proof-scope boundaries
- SHA256 manifests

This repository does not publish:

- solver source code
- private MDO/MCDO internals
- rule selection logic
- branch ordering
- branch scoring
- private search strategy
- acceleration mechanisms

## Boundary statement

This repository does not claim to solve open Ramsey numbers.

For R(5,5), the McKay r55_42some.g6 file is treated as a known reference sample, not as a complete catalogue.

## Reference

Public Ramsey graph catalogues:

https://users.cecs.anu.edu.au/~bdm/data/ramsey.html

## License and ownership

© 2026 Michał Machura

Results, validation tables, figures, certificates, and public documentation are licensed under CC BY 4.0.

Solver implementation not released.

The MDO/MCDO solver source code, internal search strategy, rule selection logic, branch scoring, and private method structure are not included in this repository and are not licensed for use.


## Figures

Selected public Ramsey graph figures are available in the `figures/` directory.

Included figures:

- R(3,3), K5 lower-bound witness
- R(3,4), K8 lower-bound witness
- R(3,5), K13 unique lower-bound witness
- R(3,6), K17 all 7 known graphs
- R(4,4), K17 lower-bound witness
- R(3,9), K35 unique graph
- R(5,5), K42 known reference example and complement

These figures are documentation artifacts. They do not disclose the private solver implementation.
