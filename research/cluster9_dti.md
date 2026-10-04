# Cluster 9: AI/ML for Genomics — Drug-Target Interaction (DTI) Prediction

## Overview

Drug-target interaction (DTI) prediction is a critical component of computational drug discovery, enabling identification of new drug candidates, drug repurposing, and off-target effect prediction. The field has evolved from traditional matrix factorization and similarity-based methods to sophisticated deep learning architectures including graph neural networks, transformers, and large language models.

---

## State-of-the-Art Approaches

| Method | Year | Key Innovation | Type |
|--------|------|----------------|------|
| DeepDTA | 2018 | CNN on SMILES + protein sequences | Deep Learning |
| GraphDTA | 2021 | GNN on molecular graphs | Graph Neural Network |
| MGraphDTA | 2022 | 27-layer multiscale GNN with dense connections | Deep GNN |
| M3ST-DTI | 2025 | Multi-task learning, multi-modal (text/structural/functional) | Multi-modal DL |
| LLM3-DTI | 2025 | LLM + multi-modal data co-powered framework | LLM-based |
| EviDTI | 2025 | Evidential deep learning for uncertainty quantification | Uncertainty-aware |
| EBD-DTI | 2026 | Episodic bridge diffusion for zero-shot cold-start | Graph + Diffusion |
| ColdstartMHDTI | 2026 | Pretraining + attention-based heterogeneous graph | Graph + Pretraining |
| Komet | 2024 | Kronecker-optimized method with Nyström approximation | Scalable ML |
| DTI-RME | 2025 | Robust multi-kernel ensemble | Ensemble |
| SSCPA-DTI | 2025 | Substructure subsequences + cross co-attention | Attention-based |
| GraphTransDTI | 2025 | Graph transformer + CNN-BiLSTM hybrid | Hybrid |
| GADFDTI | 2025 | Gated-attention dual-fusion | Fusion-based |
| GTStrDTI | 2026 | Structure-aware graph attention hierarchical transformer | Transformer |

---

## Bottlenecks

1. **Data Imbalance**: Positive (known interactions) vs negative (unknown) samples are highly imbalanced, typically 1:5 to 1:10 ratios, biasing models toward negative predictions.
2. **Cold-Start Problem**: Predicting interactions for entirely unseen drugs or proteins remains a critical challenge. Graph-based models fail because new nodes have no edges for message passing.
3. **Uncertainty Quantification**: Most deep learning models produce overconfident predictions without reliable confidence estimates, leading to false positives in experimental validation.
4. **Cross-Modal Alignment**: Effectively fusing drug molecular representations (graphs/SMILES) with protein sequence representations remains difficult; simple concatenation loses interaction patterns.
5. **Scalability**: Training on large-scale datasets (BindingDB, DrugBank with millions of interactions) requires significant computational resources.
6. **Training-Test Distribution Mismatch**: Standard random splits overestimate performance; entity-disjoint (cold-start) evaluation reveals significant performance drops.
7. **Protein Representation Generalization**: Protein representations generalize poorly to unseen targets due to localized binding pockets that full-sequence mean pooling dilutes.

---

## NP-Hard Problems

The DTI prediction problem itself is typically formulated as binary classification or regression, not directly as an NP-hard problem. However, several related computational problems in drug discovery are NP-hard:

- **Molecular Docking**: Predicting optimal ligand-protein binding conformation is NP-hard due to the combinatorial search space of rotatable bonds and binding poses.
- **Protein Folding**: Predicting 3D protein structure from sequence (Levinthal's paradox) is NP-hard in its general form.
- **Substructure Search**: Maximum common substructure detection between molecules is NP-hard.
- **General NP-Hardness Framework**: The MIT 6.046J recitation on NP-hardness provides the theoretical foundation for proving computational intractability of related combinatorial optimization problems in drug design.

---

## Open-Source Projects

| Project | Description | URL |
|---------|-------------|-----|
| DeepDTA | CNN-based DTI prediction (305 GitHub stars) | https://github.com/hkmztrk/DeepDTA |
| GraphDTA | GNN-based drug-target binding affinity prediction | https://github.com/thinng/GraphDTA |
| Komet | Scalable DTI prediction with GPU parallel computation | Open-source (paper: PMC11423346) |
| RDKit | Chemical informatics toolkit for molecular featurization | https://www.rdkit.org |
| DTI-RME | Robust multi-kernel ensemble DTI predictor | Available from authors |
| EBD-DTI | Episodic bridge diffusion for zero-shot DTI | Available from authors |

---

## Hardware Requirements

- **GPU Acceleration**: Provides 55–179× speedup over CPU for DTI model training. Dataset E (4,389 training samples): CPU 53.9 min vs GPU 30.6 s.
- **Training Time**: ~6.5 hours per model on CPU cluster (Intel Xeon @ 2.60 GHz, 16 parallel Slurm jobs).
- **Memory**: Minimum 32 GB RAM for preprocessing; GPU memory scales with model depth and batch size.
- **Mixed Precision**: Reduces GPU memory by ~40% and accelerates training by 3× (PyTorch AMP).
- **Inference**: CPU-only PyTorch sufficient for linear models (~3 min/model); GPU needed for non-linear modules (~3.8 min/model).
- **HPC**: Slurm-based clusters recommended for ensemble training and cross-validation.

---

## Cost Tradeoffs

| Approach | Compute Cost | Accuracy | Scalability |
|----------|-------------|----------|-------------|
| Matrix Factorization | Low | Moderate | High |
| Deep Learning (CNN/GNN) | High | High | Moderate |
| Transformer-based | Very High | Very High | Low-Moderate |
| LLM-based | Very High | High (emerging) | Low |
| Komet (scalable ML) | Moderate | High | Very High |
| Ensemble methods | High | High | Moderate |

- **GPU vs CPU**: 179× speedup justifies GPU hardware investment for large-scale screening.
- **Pre-trained models**: Better zero-shot performance but larger memory footprint and inference cost.
- **Scalability vs Accuracy**: Komet demonstrates that efficient approximations (Nyström) can maintain accuracy while scaling to very large datasets.

---

## Scalability Limits

1. **GAT Quadratic Complexity**: Graph attention mechanisms incur O(n²) time and memory complexity with respect to adjacency matrix size, limiting deployment at scale.
2. **Memory Demands**: Escalate rapidly with graph size and model depth; deep GNNs (27+ layers) require dense connections to mitigate over-smoothing.
3. **Dataset Size**: BindingDB contains ~2.5M interactions; DrugBank ~14K drugs and 5K targets. Training on such scales requires distributed computing.
4. **Komet's Solution**: Uses Nyström approximation and Kronecker-optimized computation to scale without compromising performance.
5. **Cold-Start at Scale**: Zero-shot inference for millions of unseen drug-target pairs remains computationally expensive.

---

## Biosecurity Considerations

1. **Dual-Use Risk**: Urbina et al. (2022, Nature Machine Intelligence) demonstrated that AI drug discovery models can be misused to design toxic molecules by inverting the optimization objective—rewarding toxicity instead of therapeutic benefit.
2. **BIOSECURE Act**: Proposed US legislation (H.R. 7085) would restrict federal agencies from contracting with biotech companies linked to foreign adversaries, impacting AI drug discovery collaborations.
3. **Nucleic Acid Synthesis Screening**: OSTP Framework (April 2024) requires screening synthetic nucleic acid sequences ≥200 bases (reducing to 50 bases by October 2026) for sequences of concern.
4. **Responsible AI**: Need for codes of conduct, employee training, secure model deployment, and cross-disciplinary discussions on AI misuse potential in drug discovery.
5. **Model Security**: Pre-trained models for toxicity/bioactivity prediction could be repurposed for harmful applications without proper access controls.

---

## Failure Modes

1. **False Positives**: Predicted interactions that do not validate experimentally. Even high-reliability predictions (L=1) show ~7% false positive rate.
2. **Overconfident Predictions**: Standard neural networks produce poorly calibrated confidence scores, leading to wasted experimental resources.
3. **Cold-Start Collapse**: Performance drops of 12–28% when predicting interactions for unseen proteins (cold-target setting).
4. **Homologue Confusion**: Predictions may map to murine homologues of human targets, creating apparent false positives.
5. **Over-Smoothing**: Deep GNNs lose discriminative power as node representations become indistinguishable with increasing layers.
6. **Distribution Shift**: Models trained on one target family (e.g., kinases) generalize poorly to others (e.g., GPCRs, nuclear receptors).
7. **Data Leakage**: Standard random cross-validation overestimates performance due to similarity between training and test compounds.

---

## Most Cited Papers

1. **Öztürk et al. (2018)** — "DeepDTA: deep drug-target binding affinity prediction" — *Bioinformatics* 34(17):i821–i829. DOI: 10.1093/bioinformatics/bty593
2. **Nguyen et al. (2021)** — "GraphDTA: predicting drug-target binding affinity with graph neural networks" — *Bioinformatics* 37(8):1140–1147. DOI: 10.1093/bioinformatics/btaa921
3. **Wang et al. (2017)** — "Large-Scale Prediction of Drug-Target Interaction: a Data-Centric Review" — *AAPS J* 19(5):1264–1275. DOI: 10.1208/s12248-017-0092-6
4. **Yang et al. (2022)** — "MGraphDTA: deep multiscale graph neural network for explainable drug-target binding affinity prediction" — *Chemical Science* 13:816–833. DOI: 10.1039/D1SC05180F
5. **Urbina et al. (2022)** — "Dual Use of Artificial Intelligence-powered Drug Discovery" — *Nature Machine Intelligence* 4(3):189–191. DOI: 10.1038/s42256-022-00465-9

---

## Key Databases

- **BindingDB**: ~2.5M drug-target binding affinities
- **DrugBank**: ~14K drugs, 5K targets
- **ChEMBL**: Bioactivity data for ~2M compounds
- **KIBA**: 2,116 drugs × 229 targets
- **Davis**: 72 drugs × 442 targets (kinase inhibitors)

---

## Summary

DTI prediction has advanced rapidly from matrix factorization to multi-modal deep learning and LLM-based frameworks. Key challenges remain in cold-start generalization, uncertainty quantification, scalability, and biosecurity. The field is trending toward pre-trained models, graph transformers, and evidential deep learning for more reliable and interpretable predictions. Computational requirements range from CPU-feasible for small models to GPU clusters for large-scale screening, with mixed-precision training and efficient approximations (Nyström, Kronecker) enabling scalability.
