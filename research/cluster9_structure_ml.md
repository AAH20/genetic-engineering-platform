# Cluster 9: AI/ML for Genomics — Protein Structure Prediction ML

**Date:** 2026-10-04
**Focus:** Protein structure prediction via machine learning

---

## 1. State-of-the-Art Approaches

| Approach | Key Method | Accuracy | Compute | Citation |
|----------|-----------|----------|---------|----------|
| AlphaFold2 | End-to-end attention + MSA + recycling | GDT ~90 (CASP14); pLDDT>70 for 98.5% human proteome | 16×A100 GPUs, ~48h for complexes | Jumper et al., Nature 2021 |
| AlphaFold3 | Pairformer + diffusion; protein/RNA/DNA/ligand | SOTA on monomers & complexes | Proprietary (AlphaFold Server only) | Abramson et al., Nature 2024 |
| RoseTTAFold | Three-track network (1D/2D/3D) | TM-score 0.91 CASP14 FM | ~3 min/300aa on RTX 4090 | Baek et al., Science 2021 |
| ESMFold | Protein language model (ESM-2, 15B params); no MSA | TM-score 0.85 CASP14 FM | Seconds; CPU possible | Lin et al., Science 2023 |
| OpenFold | PyTorch AF2 reproduction + TensorRT | TM-score 0.91 CASP14 FM | 131× faster than AF2 with TRT | bioRxiv 2026 |
| ColabFold | AF2 + MMseqs2 MSA generation | TM-score 0.90 CASP14 FM | 12 min/400aa | Mirdita et al., Nat Methods 2022 |
| SeedFold | Width-scaled Pairformer (512) + linear attention | lDDT 0.8889 monomer; >AF3 on most tasks | 26.5M distillation samples | arXiv 2512.24354 |
| RGN2 | AminoBERT (12-layer transformer) single-sequence | Outperforms AF2 on orphan proteins | 10^6× less compute than AF2 | PMC10440047 |

---

## 2. Most Cited Papers

1. **Jumper et al. (2021)** — "Highly accurate protein structure prediction with AlphaFold." *Nature* 596:583–589. doi:10.1038/s41586-021-03819-2
2. **Baek et al. (2021)** — "Accurate prediction of protein structures and interactions using a three-track neural network." *Science* 373:871–876.
3. **Lin et al. (2023)** — "Evolutionary-scale prediction of atomic-level protein structure with a language model." *Science* 379:1123–1130.
4. **Abramson et al. (2024)** — "Accurate structure prediction of biomolecular interactions with AlphaFold 3." *Nature* 630:493–500.
5. **AlQuraishi (2019)** — "ProteinNet: a standardized data set for machine learning of protein structure." *BMC Bioinformatics* 20:311.
6. **Senior et al. (2020)** — "Improved protein structure prediction using potentials from deep learning." *Nature* 577:706–710.
7. **Meng et al. (2025)** — "Protein structure prediction via deep learning: an in-depth review." *PMC12003282*.
8. **Hunter (2024)** — "Security challenges by AI-assisted protein design." *EMBO Reports* 25:2168–2171.
9. **Baker & Church (2024)** — "Protein design meets biosecurity." *Science* 383:349.
10. **Zhang et al. (2026)** — "FoldMark: Safeguarding Protein Structure Generative Models." *ACM Computing Surveys*.

---

## 3. Bottlenecks

- **MSA generation bottleneck**: JackHMMer/HHblits-based MSA generation takes 30+ min per sequence; MMseqs2 reduces to ~2 min but still dominates runtime for MSA-based methods.
- **Conformational sampling**: AlphaFold predicts single conformations; alternative folds and metamorphic proteins are missed (PMC11722503).
- **Orphan proteins**: Proteins with no homologous sequences in databases cannot generate meaningful MSAs, limiting AF2/ColabFold accuracy.
- **Large proteins & complexes**: Memory scales with sequence length; 16GB VRAM handles ~800aa, 24GB ~1500aa, 40GB (A100) ~2500aa.
- **Training data scarcity**: Only ~220K experimental structures in PDB; SeedFold addresses via 26.5M-sample distillation from AF2.
- **Width bottleneck in Pairformer**: Model capacity is limited by hidden dimension of pairwise representation (128 in AF2), not depth.
- **Cubic complexity of triangular attention**: Pairformer triangular operations scale O(n³) with protein length.
- **Lack of dynamics**: Models predict static structures; conformational ensembles, allostery, and kinetics are not captured.
- **Interpretability gap**: No correlation between internal embeddings and structural outputs; coevolutionary signals may be misassigned.

---

## 4. NP-Hard Problems

| Problem | Complexity | Reference |
|---------|-----------|-----------|
| HP model folding (lattice) | NP-hard | Berger & Leighton, 1998 |
| Protein structure alignment (RMSD under correspondence) | NP-hard | Goldman et al., J. Comput. Biol. 1999 |
| Multiple structure alignment | NP-hard | Papadimitriou & Roughgarden, 2008 |
| Protein threading (fold recognition) | NP-complete | Lathrop, Protein Eng. 1994 |
| Side-chain packing (rotamer optimization) | NP-hard | Pierce & Winfree, 2002 |
| Flexible molecular docking | NP-hard | Fraenkel, 1993 |
| Contact map overlap maximization | NP-hard | (reduction from MAX-CLIQUE) |

**Implication**: Exact solutions are computationally prohibitive for proteins >100 residues; all practical methods rely on heuristics, approximations, or learned representations.

---

## 5. Failure Modes

1. **Fold-switching proteins**: AF2 predicts only dominant conformation; alternative folds are low-confidence or absent (PMC11722503).
2. **Homologs with divergent folds**: Similar sequences can evolve distinct folds; MSA-based methods misled by training-set homologs.
3. **Designed/orphan proteins**: No MSA available; single-sequence methods (ESMFold, RGN2) needed but less accurate.
4. **Low-confidence regions**: pLDDT <70 indicates disorder or uncertainty; ~1.5% of human proteome has low-confidence regions.
5. **Over-reliance on templates**: AF2 may copy training-set structures rather than learn folding physics.
6. **Stochastic sampling**: Alternative conformation sampling (AFsample2) shows no correlation between embeddings and outputs.
7. **Experimental validation gap**: Predicted active-site geometry inaccuracies; wet-lab confirmation still required.
8. **Force field limitations**: MD-based refinement fails for large proteins; energy landscape lacks funnel-like shape.

---

## 6. Hardware Requirements

| Platform | Hardware | Use Case | Cost |
|----------|----------|----------|------|
| AlphaFold3 Server | 16×A100, ~48h queue | Complex predictions | Free (academic) |
| OpenFold-TRT | 1× RTX PRO 6000 Blackwell | 131× faster than AF2 | ~$15K GPU |
| ColabFold | 1× RTX 4090 (24GB) | 12 min/400aa | ~$1.6K GPU |
| ESMFold | CPU possible | 2 min/400aa; 617M proteins/2 weeks | Minimal |
| RosettaFold | 1× RTX 4090 | 3 min monomer, 18 min dimer | ~$1.6K GPU |
| DGX Spark | ARM + small GPU | Edge/embedded | ~$5K |
| Grace Hopper GH200 | 450GB/s C2C interconnect | Large-scale MSA | ~$30K+ |

**VRAM scaling**: 16GB → ~800aa; 24GB → ~1500aa; 40GB → ~2500aa.

---

## 7. Cost Tradeoffs

| Method | Time/10K seqs | Cloud Cost/10K | Accuracy (TM) |
|--------|---------------|-----------------|---------------|
| OpenFold | 12,500 GPU-hours | ~$25,000 | 0.91 |
| ColabFold | 2,333 GPU-hours | ~$4,700 | 0.90 |
| ESMFold | 333 GPU-hours | ~$670 | 0.85 |
| AF2 baseline | 44.66 sec/inference | ~500 years (1 GPU) | 0.91 |
| OpenFold-TRT | 4.5 months (500 GPUs) | — | 0.91 |

**Key insight**: ESMFold is 37× cheaper than ColabFold and 375× cheaper than OpenFold for large-scale prediction, at modest accuracy cost.

---

## 8. Scalability Limits

- **AF2 baseline**: 350M sequences × 44.66 sec = ~500 years on 1 GPU; 1 year on 500 GPUs.
- **OpenFold-TRT**: 4.5 months on 500 GPUs (131× speedup).
- **ESMFold**: 617M metagenomic proteins in 2 weeks (Meta, 2023).
- **SeedFold**: Scales to 512-width Pairformer; 26.5M distillation samples.
- **Linear attention**: Reduces triangular complexity from O(n³) to O(n²).
- **ARM optimization**: Grace Hopper enables MSA generation beyond GPU RAM limits.
- **Data scaling**: Distillation from AF2 expands training set 100× beyond experimental structures.

---

## 9. Biosecurity Governance

- **Dual-use risk**: AI protein design enables creation of pandemic-capable proteins (Hunter, EMBO Reports 2024).
- **Screening gap**: Current DNA synthesis screening relies on homology; de novo proteins evade detection (Baker & Church, Science 2024).
- **Proposed safeguards**:
  - Collect and store synthetic gene sequence data for emergency screening (Baker & Church, 2024).
  - Integrate screening with synthesis process itself.
  - Structure-based homology prediction for novel sequences.
  - Controlled, monitored access to AI protein design tools.
- **FoldMark**: Watermarking strategy for protein generative models; >95% bit accuracy at 32 bits; traces up to 1M users (Zhang et al., 2026).
- **Governance frameworks**: Wang et al. (2025) call for built-in biosecurity safeguards for generative AI tools in *Nature Biotechnology*.
- **AI for non-proliferation**: ML capabilities to detect and limit proliferation (Kosal, Georgia Tech).

---

## 10. Open-Source Projects

| Project | GitHub | Stars | License | Description |
|---------|--------|-------|---------|-------------|
| AlphaFold | deepmind/alphafold | 13K+ | Apache-2.0 | AF2 inference code & weights |
| OpenFold | aqlaboratory/openfold | 3,376+ | Apache-2.0 | Trainable PyTorch AF2 reproduction |
| ColabFold | soedinglab/ColabFold | 2,789+ | MIT | AF2 + MMseqs2 for fast prediction |
| ESMFold | facebookresearch/esm | 4,118+ | MIT | Protein language model folding |
| RoseTTAFold | RosettaCommons/RoseTTAFold | 2K+ | MIT | Three-track network folding |
| ProteinNet | — | — | — | Standardized ML training datasets |
| RGN2 | — | — | — | Single-sequence prediction via AminoBERT |
| SeedFold | — | — | — | Scaled Pairformer with linear attention |
| FoldMark | — | — | — | Watermarking for protein generative models |
| MMseqs2 | soedinglab/MMseqs2 | 1K+ | MIT | Fast MSA generation for ColabFold |

---

## 11. Summary

Protein structure prediction has been transformed by deep learning, with AlphaFold2 achieving near-experimental accuracy for single-domain proteins. Key advances include:

- **Accuracy**: AF2/AF3, RoseTTAFold, OpenFold achieve TM-score >0.90 on CASP14 free-modeling targets.
- **Speed**: ESMFold enables metagenomic-scale prediction (617M proteins/2 weeks); OpenFold-TRT achieves 131× speedup.
- **Scalability**: Linear attention and width-scaling (SeedFold) push the boundaries of model capacity.
- **Accessibility**: ColabFold and ESMFold bring prediction to consumer hardware.

**Remaining challenges**: Alternative conformations, orphan proteins, conformational dynamics, interpretability, and biosecurity governance.

---

## References

1. Jumper J, et al. Highly accurate protein structure prediction with AlphaFold. *Nature*. 2021;596:583-589.
2. Baek M, et al. Accurate prediction of protein structures and interactions using a three-track neural network. *Science*. 2021;373:871-876.
3. Lin Z, et al. Evolutionary-scale prediction of atomic-level protein structure with a language model. *Science*. 2023;379:1123-1130.
4. Abramson J, et al. Accurate structure prediction of biomolecular interactions with AlphaFold 3. *Nature*. 2024;630:493-500.
5. AlQuraishi M. ProteinNet: a standardized data set for machine learning of protein structure. *BMC Bioinformatics*. 2019;20:311.
6. Senior AW, et al. Improved protein structure prediction using potentials from deep learning. *Nature*. 2020;577:706-710.
7. Meng Y, et al. Protein structure prediction via deep learning: an in-depth review. *PMC*. 2025;PMC12003282.
8. Hunter P. Security challenges by AI-assisted protein design. *EMBO Reports*. 2024;25:2168-2171.
9. Baker D, Church G. Protein design meets biosecurity. *Science*. 2024;383:349.
10. Zhang Z, et al. FoldMark: Safeguarding Protein Structure Generative Models. *ACM Computing Surveys*. 2026.
11. Dai W, et al. Applying Deep Reinforcement Learning to the HP Model for Protein Structure Prediction. *arXiv*. 2022;2211.14939.
12. OpenFold-TRT: Efficient protein structure prediction from compact computers to datacenters. *bioRxiv*. 2026.
13. SeedFold: Scaling Biomolecular Structure Prediction. *arXiv*. 2025;2512.24354.
14. Proteins with alternative folds reveal blind spots in AlphaFold-based protein structure prediction. *PMC*. 2024;PMC11722503.
15. Protein structure prediction powered by artificial intelligence. *PMC*. 2025;PMC13006253.
