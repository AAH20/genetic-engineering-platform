# Cluster 6: Flux Balance Analysis (FBA) — Research Summary

## Overview

Flux Balance Analysis (FBA) is a constraint-based optimization framework for predicting steady-state metabolic flux distributions in genome-scale metabolic models (GEMs). It solves the linear program: maximize cᵀv subject to S·v = 0 and lb ≤ v ≤ ub, where S is the stoichiometric matrix, v is the flux vector, and c is the objective function (typically biomass production). FBA requires no kinetic parameters, making it scalable to networks with thousands of reactions.

## Most Cited Papers

1. **Orth, Thiele & Palsson (2010)** — "What is flux balance analysis?" *Nature Biotechnology* 28:245-248. The canonical FBA primer; describes the COBRA Toolbox, core assumptions (steady-state, optimality), and applications in physiological studies, gap-filling, and synthetic biology.

2. **Burgard, Pharkya & Maranas (2003)** — "OptKnock: A bilevel programming framework for identifying gene knockout strategies for microbial strain optimization." *Biotechnology & Bioengineering*. Introduced the bilevel MILP framework for coupling growth with chemical production; foundational for computational strain design.

3. **Edwards & Palsson (1998)** — "The Escherichia coli MG1655 in silico metabolic genotype: its definition, characteristics, and capabilities." *PNAS*. Early genome-scale metabolic reconstruction establishing the FBA framework.

4. **Feist et al. (2007)** — "A genome-scale metabolic reconstruction for Escherichia coli K-12 MG1655 that accounts for 1260 ORFs and thermodynamic information." *Molecular Systems Biology*. iAF1260 model; widely used for FBA studies.

5. **Monk et al. (2017)** — "iML1515, a knowledgebase that computes Escherichia coli traits." *Nature Biotechnology*. Current gold-standard E. coli GEM with 2,719 reactions, 1,192 metabolites, 1,515 genes.

## SOTA Approaches

| Approach | Description | Scale |
|----------|-------------|-------|
| **COBRApy** | Python package for constraint-based modeling; FBA, FVA, pFBA, dFBA, gene deletions, flux sampling | Genome-scale |
| **COBRA Toolbox** | MATLAB toolbox with 350+ methods; the original FBA platform | Genome-scale |
| **RAVEN Toolbox** | MATLAB toolbox for model reconstruction and analysis | Genome-scale |
| **OptKnock** | Bilevel MILP for identifying gene knockout strategies coupling growth to production | Genome-scale (MILP-limited) |
| **FVA** | Flux Variability Analysis — computes min/max flux for each reaction at optimal objective | 2n LPs |
| **pFBA** | Parsimonious FBA — minimizes total flux while maintaining objective optimality | Genome-scale |
| **dFBA** | Dynamic FBA — iteratively solves FBA with updated environmental constraints | Genome-scale, temporal |
| **MOMA/ROOM** | Minimization of metabolic adjustment / regulatory on/off minimization for perturbation analysis | Genome-scale |
| **GIMME/iMAT/E-Flux** | Omics integration methods for context-specific models | Genome-scale |
| **GDLS** | Genetic Design through Local Search — heuristic for large-scale strain design | Genome-scale, linear scaling |
| **FBApro** | Linear transformation alternative to optimization; orders of magnitude faster | Genome-scale |
| **ChemoCalib** | Multiblock PLS calibration of GEMs from multi-omics data | Genome-scale |
| **gsMOBO** | Multiobjective Bayesian optimization for media design with GEMs | Genome-scale |
| **pycFBA** | Conditional FBA for cyclic environments (diurnal, feast-famine) | Genome-scale |

## Bottlenecks

1. **Solution degeneracy**: FBA LPs are often highly degenerate — many flux distributions achieve the same objective value. FVA is needed to characterize the solution space but requires solving 2n LPs.

2. **No kinetic parameters**: FBA cannot predict metabolite concentrations or dynamic behavior. It is limited to steady-state analysis.

3. **Objective function dependence**: Predictions are highly sensitive to the choice of objective function (biomass, ATP, etc.). No universal objective captures all conditions.

4. **Missing regulatory effects**: FBA does not account for transcriptional regulation, post-translational modifications, or enzyme activation/inhibition.

5. **Thermodynamically infeasible loops**: Standard FBA allows internal loops that violate the second law of thermodynamics, requiring additional constraints (loopless FBA, TFBA).

6. **MILP scalability**: Strain design via bilevel optimization (OptKnock) converts to MILP, which scales exponentially with the number of allowed manipulations. Global search becomes prohibitive beyond a few knockouts.

7. **Omics integration gap**: Expression-to-flux heuristics (E-Flux, GIMME, iMAT) ignore cross-omics covariance and lack uncertainty propagation, yielding limited agreement with 13C-MFA measurements.

8. **Model reconstruction quality**: GEMs contain gaps, missing reactions, and incorrect annotations that propagate to predictions.

## NP-Hard Problems

- **Characterizing the optimal solution space of FBA** is NP-hard (explicitly stated in Klamt & Gilles, 2008, and related work).
- **Elementary Flux Mode (EFM) enumeration** is NP-hard; limited to networks of ≤100 reactions.
- **Bilevel optimization** (OptKnock) → MILP is NP-hard; runtime scales exponentially with manipulations.
- **Minimal Cut Sets (MCSs)** computation is NP-hard; used for identifying failure modes in metabolic networks.
- **Loopless FBA** requires MILP with binary variables, making it NP-hard.

## OSS Projects

| Project | Language | Description |
|---------|----------|-------------|
| **COBRApy** | Python | Primary open-source FBA platform; pip-installable; SBML/JSON/YAML I/O |
| **COBRA Toolbox** | MATLAB | Original FBA toolbox; 350+ methods; widely cited |
| **RAVEN Toolbox** | MATLAB | Model reconstruction, FBA, FVA, gap-filling |
| **BiGG Models** | Database | 100+ curated GEMs for download |
| **Escher** | JavaScript | Web-based flux map visualization |
| **Fluxer** | Web | Browser-based FBA tool |
| **pycFBA** | Python | Conditional FBA for cyclic environments |
| **OptKnock/GDLS** | MATLAB/Python | Strain design algorithms |
| **GLPK** | C | Open-source LP/MILP solver (single-threaded) |
| **SCIP** | C | Open-source constraint integer programming solver |

## Hardware Requirements

- **Basic FBA**: LP solves in milliseconds on a standard laptop; genome-scale models (2,000+ reactions) are trivial for modern hardware.
- **FVA**: Requires 2n LP solves; seconds to minutes for genome-scale models. Parallelization across reactions provides near-linear speedup.
- **MILP strain design**: Hours to days for genome-scale models with multiple manipulations. Global MILP search (OptKnock) is the bottleneck.
- **Memory**: Stoichiometric matrices range from ~1,200×2,700 (iML1515) to ~4,100×13,500 (Recon3D). Sparse matrix representations keep memory manageable.
- **Solver threading**: GLPK is single-threaded (12-13% CPU on quad-core). Gurobi and CPLEX exploit multi-core architectures.
- **Cloud computing**: Large-scale strain design and parameter scans benefit from cloud HPC clusters.

## Cost Tradeoffs

- **Open-source vs commercial solvers**: GLPK and SCIP are free but slower and less numerically stable than Gurobi/CPLEX. Commercial licenses cost thousands of dollars annually.
- **Optimality vs runtime**: GDLS finds comparable solutions to OptKnock with >10× speedup but sacrifices global optimality guarantees.
- **FVA cost**: 2n LP solves make FVA expensive for large models; fastFVA and VFFVA reduce this via warm-starts and parallelization.
- **Surrogate ML models**: Pre-trained ML surrogates can replace FBA calculations with 100× speedup, but require offline training data generation for each model modification.
- **Omics integration**: Experimental validation (13C-MFA) is expensive but necessary for calibrating FBA predictions.

## Scalability Limits

- **FBA (LP)**: Polynomial time; scales to genome-scale models with 10,000+ reactions. Millions of simulations feasible.
- **FVA**: Scales linearly with number of reactions (2n LPs). Parallelization essential for large models.
- **MILP strain design**: Exponential scaling with number of manipulations. Practical limit: ~5-10 knockouts for global search on genome-scale models.
- **EFM enumeration**: Limited to ≤100 reactions due to combinatorial explosion.
- **dFBA**: Requires solving FBA at each time step; runtime scales with simulation duration and number of steps.
- **Community models**: Multi-species FBA scales with the product of community members' network sizes.

## Biosecurity Governance

- FBA and GEMs can predict metabolic capabilities of pathogens, including potential for enhanced virulence or production of toxic compounds.
- Strain design tools (OptKnock, GDLS) could theoretically be misused to optimize pathogens for enhanced growth or toxin production.
- Responsible use requires institutional oversight, particularly for work with select agents or dual-use research of concern (DURC).
- Publication of strain design strategies for pathogenic organisms should consider biosecurity implications.
- The COBRA Toolbox and COBRApy are dual-use tools with both beneficial and potential misuse applications.

## Failure Modes

1. **Incorrect objective function**: Wrong objective leads to biologically implausible flux distributions. No single objective is universally correct.
2. **Model gaps**: Missing reactions or incorrect annotations produce false predictions. Gap-filling can introduce artifacts.
3. **Thermodynamically infeasible loops**: Standard FBA allows loops that violate thermodynamics, leading to unrealistic flux ranges.
4. **Poor experimental agreement under stress**: FBA predictions degrade under stress, overflow metabolism, or regulatory conditions not captured by stoichiometry.
5. **Degeneracy in futile cycles**: Futile cycles generate FBA degeneracy, making flux predictions unreliable without additional constraints.
6. **Omics integration failure**: Expression-to-flux heuristics may not reflect true biology; ChemoCalib showed only Spearman ρ = 0.461 vs 13C-MFA even with multi-omics calibration.
7. **Dynamic environment mismatch**: Static FBA cannot capture transient behaviors; dFBA partially addresses this but adds computational cost.
8. **Strain design prediction failure**: OptKnock predictions may not match experimental results (e.g., B. subtilis 2,3-butanediol case where experimental data did not confirm predictions).

## MILP in FBA

- **OptKnock**: Bilevel optimization (upper: maximize product; lower: maximize biomass) converted to MILP via duality theory. Uses binary variables for gene knockouts.
- **TFBA (Thermodynamic FBA)**: Adds binary variables to enforce thermodynamic feasibility, converting FBA to MILP.
- **SubNetX**: MILP formulation for enumerating feasible heterologous pathways with minimal steps.
- **FaceCon/ShadowCon**: MILP modules for filtering strain designs based on coupling degree and shadow prices.
- **GDLS**: Uses MILP solvers (SCIP, SoPlex) within a local search framework for scalable strain design.
- **ΔFBA**: MILP formulation for predicting flux alterations from differential gene expression data.
- **MILP limitations**: Runtime scales exponentially with number of binary variables (manipulations). Practical limit: ~5-10 manipulations for genome-scale models.

## Key Citations

- Orth JD, Thiele I, Palsson BØ (2010). What is flux balance analysis? *Nature Biotechnology* 28:245-248.
- Burgard AP, Pharkya P, Maranas CD (2003). OptKnock: A bilevel programming framework for identifying gene knockout strategies. *Biotechnology & Bioengineering* 84:647-657.
- Edwards JS, Palsson BØ (1998). The Escherichia coli MG1655 in silico metabolic genotype. *PNAS* 95:5528-5533.
- Feist AM, et al. (2007). A genome-scale metabolic reconstruction for E. coli K-12 MG1655. *Molecular Systems Biology* 3:121.
- Monk JM, et al. (2017). iML1515, a knowledgebase that computes E. coli traits. *Nature Biotechnology* 35:904-908.
- Klamt S, Gilles ED (2004). Minimal cut sets in metabolic networks. *Bioinformatics* 20:226-234.
- Gudmundsson S, Thiele I (2010). Computationally efficient flux variability analysis. *BMC Bioinformatics* 11:489.
- Clark ST, Verwoerd WS (2012). Minimal cut sets and the use of failure modes in metabolic networks. *PLOS ONE* 7:e49264.
- Dromms RA, et al. (2020). LK-DFBA: A linear programming-based modeling strategy for capturing dynamics and regulation. *PLOS ONE* 15:e0236888.
- Rügen M, et al. (2015). Conditional flux balance analysis. *PLOS Computational Biology* 11:e1004621.
