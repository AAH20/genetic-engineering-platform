# Cluster 9: Variant Effect Prediction — AI/ML for Genomics

## Overview

Variant Effect Prediction (VEP) is the computational task of predicting the functional consequences of genetic variants, ranging from molecular effects (protein stability, binding affinity) to clinical pathogenicity. The field has evolved from conservation-based methods (SIFT, PolyPhen-2) through machine learning ensembles to protein language models (ESM, AlphaMissense) and large-scale genomic foundation models (AlphaGenome). A systematic review identified 118 VEPs accepting 36 variant types and predicting 161 functional impacts, with ~60% of impacts covered by just three tools (SnpEff, FAVOR, SparkINFERNO) [1].

## State-of-the-Art Approaches

| Approach | Key Innovation | Performance | Citation |
|----------|---------------|-------------|----------|
| **AlphaMissense** | AlphaFold fine-tuned on population frequency weak labels; structural context + evolutionary conservation | auROC 0.940 on ClinVar (vs 0.911 EVE); classifies 89% of missense variants | Cheng et al., *Science* 2023 [2] |
| **ESM-1b/ESM-2 PLMs** | Unsupervised protein language models; zero-shot mutation effect prediction | Outperforms SOTA on multiple benchmarks; >40k isoforms | Livesey & Marsh, *Nature Genetics* 2023 [3] |
| **AlphaGenome** | 1M bp context window; 7,000+ genomic tracks; single forward pass | SOTA on 25/26 VEP benchmarks; ~1s per variant | Google DeepMind, *Nature* 2026 [4] |
| **Sequence UNET** | Fully convolutional architecture; multi-scale representations | Comparable to ESM-1b at fraction of compute; 8.3B variants in 1.5h GPU | Genome Biology 2023 [5] |
| **PLM-SAE** | Sparse autoencoders disentangle PLM representations | 80.8% relative improvement on HECD1; +0.138 Spearman ρ | bioRxiv 2026 [6] |
| **NLR fine-tuning** | Normalised Log-odds Ratio head on DMS data | Consistent gains across ProteinGym & ClinVar | arXiv 2024 [7] |

## Bottlenecks

1. **Mutation rate heterogeneity bias**: Most VEPs rely on sequence conservation, conflating mutation rate variation with functional constraint. PhyloP scores correlate strongly with mutation rate even at neutral sites, creating systematic confounding [8].
2. **Gene-by-gene performance variation**: A model may separate benign/pathogenic perfectly in some genes (TP53, ~350 annotated variants) while making numerous errors in others (KCNJ10, 16 labels) [9].
3. **Variant type coverage gaps**: Gene fusions unsupported; variant types not equally represented across tools; non-coding variants (98% of genome) poorly addressed [1].
4. **Training data circularity**: Models trained on ClinVar annotations risk circularity when evaluated on the same source; PS1/PM5 criteria should not be used with models that saw the same position during training [9].
5. **VUS resolution bottleneck**: >90% of missense variants across ~4,000 disease-associated genes are Variants of Uncertain Significance; experimental data lacking for most [10].
6. **Computational cost asymmetry**: SIFT4G took 22 min and FoldX 232 h to predict all 24,187 variants of SARS-CoV-2 Spike; ESM-based methods require one forward pass per sequence [5].

## NP-Hard Problems

- **Combinatorial variant space**: The space of possible variants grows as 20^L for protein length L; exhaustive fitness landscape mapping is intractable for even modest protein lengths.
- **Epistasis and higher-order interactions**: Predicting effects of variant combinations requires modeling non-additive interactions, which is computationally hard (related to protein design inverse folding problems).
- **Whole-genome regulatory prediction**: Inferring the effect of a single nucleotide change across 3 billion base pairs of context with long-range regulatory interactions is a combinatorial search problem [4].
- **MSA depth vs. generalization tradeoff**: The accuracy of MSA-based methods scales with homolog coverage, but the relationship is non-linear and protein-specific.

## Open-Source Tools

| Tool | Variant Types | Functional Impacts | Notes |
|------|--------------|-------------------|-------|
| **SnpEff** | 7 | 58 (most comprehensive) | Cingolani et al. 2012 [1] |
| **FAVOR** | — | 40+ | Annotation database [1] |
| **SparkINFERNO** | — | 40+ | [1] |
| **Ensembl VEP** | 7 | — | McLaren et al. 2016 [1] |
| **DECIPHER** | 7 | — | Bragin et al. 2014 [1] |
| **SIFT/SIFT4G** | 1 | 1 | Conservation-based; widely cited [1] |
| **PolyPhen-2** | 1 | 1 | >15,000 citations [11] |
| **PROVEAN** | 1 | 1 | [11] |
| **DEOGEN2** | 1 | 1 | ML-based [11] |
| **Sequence UNET** | — | — | Python package; scalable CNN [5] |

## Hardware Requirements

- **Sequence UNET**: 1.5 h on GPU (batch size 100) or 50.9 h CPU-only for 8.3B variants across 904,134 proteins; runs on modest hardware [5].
- **AlphaGenome**: Processes 1M DNA base pairs and outputs predictions across 7,000+ tracks in ~1 second [4].
- **ESM-2**: Single forward pass per sequence with unmasked-marginal scoring; extremely scalable [3].
- **SIFT4G**: 22 min for all 24,187 SARS-CoV-2 Spike variants [5].
- **FoldX**: 232 h for same task (physics-based, not ML) [5].
- **AlphaMissense**: Pre-computed database of all possible human missense variants available as free resource [2].

## Cost Tradeoffs

- **Sequence UNET vs. ESM-1b**: Comparable pathogenicity prediction performance at significantly lower computational cost; CNN architecture is length-independent [5].
- **Meta-predictors**: High average quality but require running multiple tools; ensemble approaches (e.g., AlphaMissense combining structural + evolutionary + population data) achieve best single-model performance [2, 11].
- **Experimental (MAVE) vs. computational**: Multiplexed assays provide critical evidence but are expensive; the IGVC consortium generated experimental data for 62,215 variants across 10 genes plus 193,139 community measurements, enabling reclassification of 75% of VUS with <1% error [10].
- **Pre-computed databases**: AlphaMissense provides free proteome-wide predictions, eliminating per-query compute costs for missense variants [2].

## Scalability Limits

- **Sequence UNET**: Demonstrated at 8.3 billion variants in 904,134 proteins; 1.5 h GPU / 50.9 h CPU [5].
- **AlphaGenome**: 1M bp context window; whole-genome analysis would require tiling [4].
- **PLM-SAE**: Validated across 114 DMS datasets; target-specific gating improves >80% of datasets [6].
- **VUS resolution**: Scalable workflow reclassified 75% of 16,115 VUS across 40 genes; 62% of >90,000 unobserved variants had sufficient evidence for pre-classification [10].
- **Proteome-wide prediction**: AlphaMissense provides all possible single amino acid substitutions in the human proteome [2].

## Biosecurity & Governance

- **Guidelines for releasing a VEP**: The AVE (Analysis, Modeling, and Prediction) workstream provides recommendations for releasing novel VEPs, focusing on pathogenicity/fitness scoring tools; applicable to splicing, stability, binding affinity, and aggregation predictors [12].
- **Clinical integration**: 75 VEPs predict pathogenicity and can be used within ACMG/AMP guidelines; however, weight of computational evidence should reflect training data sources and model performance [1, 9].
- **Variant-to-Phenotype (V2P)**: Multi-task ML model predicting variant pathogenicity conditioned on disease phenotype; addresses the limitation that current methods do not differentiate between pathogenic variants causing different disease outcomes [13].
- **Dual-use considerations**: VEP tools could theoretically be used to predict effects of engineered variants; governance frameworks should balance open science with responsible release [12].

## Failure Modes

1. **Mutation rate confounding**: Conservation-based methods misinterpret mutation rate variation as functional importance; phyloP scores biased even at putatively neutral sites [8].
2. **Gene-specific failure**: Performance varies dramatically across genes; models may have high AUC genome-wide but fail in specific genes with few labels [9].
3. **Training-test circularity**: Models trained on ClinVar annotations evaluated on same source inflate performance; PS1/PM5 criteria must not be used with models that saw the same position [9].
4. **Non-coding blind spot**: Most VEPs focus on missense variants; regulatory and splicing variants poorly covered; 98% of genome is non-coding [1, 4].
5. **Redundancy across tools**: Most "likely pathogenic" AlphaMissense variants are also predicted deleterious by ≥1 of five common annotation methods; limited orthogonal information [14].
6. **Calibration gaps**: ClinGen validation strategy has limitations; gene-by-gene assessment needed but limited by label availability [9].

## Most Cited Papers

1. **Cheng et al. (2023)**. "Accurate proteome-wide missense variant effect prediction with AlphaMissense." *Science* 381:eadg7492. doi:10.1126/science.adg7492 [2]
2. **Riccio et al. (2024)**. "Variant effect predictors: a systematic review and practical guide." PMC11098935. PMID: 38573379 [1]
3. **Livesey et al. (2024)**. "Guidelines for releasing a variant effect predictor." PMC11998465. Cited by 35 [12]
4. **Livesey & Marsh (2023)**. "Advancing variant effect prediction using protein language models." *Nature Genetics* 55:1632–1643. doi:10.1038/s41588-023-01470-3 [3]
5. **Sequence UNET (2023)**. "High-throughput deep learning variant effect prediction with Sequence UNET." *Genome Biology* 24:127. doi:10.1186/s13059-023-02948-3 [5]
6. **Pejaver et al. (2024)**. "Toward trustable use of machine learning models of variant effects in the clinic." PMC11639075 [9]
7. **Cheng et al. (2023)** AlphaMissense supplementary: auROC 0.940 on 18,924 ClinVar test variants [2]
8. **Stein et al. (2025)**. "Expanding the utility of variant effect predictions with phenotype information." PMID: 41315332 [13]

## Citations

[1] Riccio C, Jansen ML, Guo L, Ziegler A. "Variant effect predictors: a systematic review and practical guide." PMC11098935, 2024.
[2] Cheng J, Novati G, Pan J, et al. "Accurate proteome-wide missense variant effect prediction with AlphaMissense." *Science* 2023;381:eadg7492.
[3] Livesey B, Marsh JA. "Advancing variant effect prediction using protein language models." *Nature Genetics* 2023;55:1632–1643.
[4] "How AlphaGenome Tackles Variant Effect Prediction." rewire.it, 2026.
[5] "High-throughput deep learning variant effect prediction with Sequence UNET." *Genome Biology* 2023;24:127.
[6] "Improving Variant Effect Prediction by Steering Sparse Mechanistic Features in Protein Language Models." bioRxiv 2026.05.12.724472.
[7] "Fine-tuning protein language models with deep mutational scanning improves variant effect prediction." arXiv:2405.06729, 2024.
[8] "Mutation rate heterogeneity biases variant effect prediction and reveals genuine mutational robustness." PMID: 42692014.
[9] "Toward trustable use of machine learning models of variant effects in the clinic." PMC11639075.
[10] "A scalable approach to resolving variants of uncertain significance." bioRxiv 2026.02.14.705848.
[11] "Assessment of variant effect predictors unveils variants difficulty as a critical performance indicator." bioRxiv 2024.07.08.602580.
[12] Livesey B, et al. "Guidelines for releasing a variant effect predictor." PMC11998465, 2024.
[13] Stein D, et al. "Expanding the utility of variant effect predictions with phenotype information." PMID: 41315332, 2025.
[14] "The performance of AlphaMissense to identify genes influencing disease." *HGG Advances* 2024.
