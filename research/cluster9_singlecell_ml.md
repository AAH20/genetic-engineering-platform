# Cluster 9: Single-Cell Machine Learning

## Overview

Single-cell machine learning applies deep learning, transformers, and foundation models to high-dimensional, sparse, heterogeneous single-cell omics data (scRNA-seq, scATAC-seq, CITE-seq, spatial transcriptomics). The field has shifted from task-specific models to large-scale pretrained foundation models (scGPT, Geneformer, scVI, C2S-Scale) that enable transfer learning across cell type annotation, batch correction, perturbation prediction, and multi-omic integration.

---

## 1. Single-Cell ML Review

| # | Title | Source | Key Findings |
|---|-------|--------|--------------|
| 1 | Transformative advances in single-cell omics: comprehensive review of foundation models, multimodal integration and computational ecosystems | PMC12560279 | Reviews foundation models (scGPT, Geneformer, AIDO.Cell, scPlantFormer, scEMB, CellPLM), multimodal integration strategies, and computational ecosystems. Highlights scaling laws and zero-shot capabilities. |
| 2 | Review of Machine Learning Advancements for Single-Cell Analysis | COMPSAC 2023 | Surveys ML algorithms for low-dimensional representations, batch normalization, cell type classification, trajectory inference, GRN inference, and multimodal data integration. |
| 3 | Dr. Hongzhe Li and Haoshu Xu Develop Novel Machine Learning Framework for Single-Cell Analysis | Penn DBEI / JMLR 2025 | Introduces regression framework for covariance matrix-valued outcomes; applied to population-scale PBMC data revealing age-related gene co-expression dysregulation. |

---

## 2. Single-Cell ML NP-Hard Problems

| # | Problem | Source | Complexity |
|---|---------|--------|------------|
| 1 | Multimodal integration embedding evaluation | arXiv:2210.12385 | Embedding matrix H ∈ R^(n×d) lacks ground truth; evaluation is ill-posed. |
| 2 | Cell-type annotation as combinatorial assignment | ACM TIST 2024 | Assigning cells to types with incomplete marker information is NP-hard. |
| 3 | Gene regulatory network inference | PubMed:41028523 | Inferring GRNs from single-cell data is computationally intractable at scale. |

---

## 3. Single-Cell ML Algorithms

| # | Algorithm/Architecture | Source | Application |
|---|------------------------|--------|-------------|
| 1 | Autoencoders (AE), VAEs, GANs, Transformers, GNNs | PMC12886477 | Imputation, clustering, batch correction, cell-type annotation |
| 2 | scGPT (generative pre-trained transformer) | bioRxiv:2023.04.30.538439 | Cell type annotation, multi-batch integration, perturbation prediction |
| 3 | C2S-Scale (Cell2Sentence LLM, 410M–27B params) | bioRxiv:2025.04.14.648850 | Scaling laws for LLMs in single-cell analysis; perturbation response, natural language interpretation |
| 4 | scVI/scANVI (variational inference) | PMC8769926 | Batch correction, cell annotation, multi-omics integration |
| 5 | mLLMCelltype (multi-LLM consensus) | GitHub:cafferychen777/mLLMCelltype | Cell type annotation using 10+ LLMs; 77.2% mean accuracy across 49 datasets |
| 6 | Hybrid CNN-Transformer for label-free phenotyping | arXiv:2605.14717 | WBC classification (91.3% accuracy) and protein-expression regression from DPC images |

---

## 4. Single-Cell ML Open-Source Software Tools

| # | Tool | Source | Description |
|---|------|--------|-------------|
| 1 | Scanpy | multiomeacademy.com/sc-toolkit | Core scverse framework for preprocessing, PCA, clustering, DE testing; scales to large atlases |
| 2 | Seurat | multiomeacademy.com/sc-toolkit | R toolkit for QC, normalization, integration, clustering, spatial workflows |
| 3 | scVI/scANVI/totalVI | Bio Open Science Index | Probabilistic VAE framework for batch correction, cell annotation, multi-omics integration |
| 4 | scGPT | GitHub:bowang-lab/scGPT | 53M parameter transformer pretrained on 33M cells; multi-task fine-tuning |
| 5 | Geneformer | PubMed:41028523 | Transformer foundation model for gene network inference and cell embedding |
| 6 | rapids-singlecell | sc-best-practices.org | GPU-accelerated single-cell analysis; cuVS ANN backends |
| 7 | LIGER | multiomeacademy.com/sc-toolkit | iNMF-based integrative non-negative factorization for dataset alignment |
| 8 | CellRank | Bio Open Science Index | Probabilistic framework for cell fate decisions and trajectory dynamics |
| 9 | mLLMCelltype | GitHub:cafferychen777/mLLMCelltype | Multi-LLM consensus for cell type annotation; integrates with Scanpy/Seurat |
| 10 | scDataset | arXiv:2506.01883 | PyTorch data loader for 100M+ cell datasets; quasi-random sampling |

---

## 5. Single-Cell ML Hardware Requirements

| # | Requirement | Source | Details |
|---|-------------|--------|---------|
| 1 | GPU VRAM | sc-best-practices.org | 24–80 GB for 50k–1M cells; >1M cells requires multi-GPU with dask-cuda |
| 2 | Dense matrix size | sc-best-practices.org | 1M cells × 30k genes = ~120 GB dense float32 — exceeds single GPU VRAM |
| 3 | CPU cores | Caltech HPC | 8–16 CPUs per GPU for data loading |
| 4 | System RAM | Caltech HPC | 32 GB minimum; 64–128 GB for large models |
| 5 | GPU models | Caltech HPC | H100 (80 GB), H200 (141 GB) for LLMs; V100 (32 GB), L40s (48 GB) for standard DL |
| 6 | AMD Instinct | ROCm docs | MI300X (192 GB), MI250X (128 GB) for memory-intensive AI workloads |

---

## 6. Single-Cell ML Cost Analysis

| # | Cost Factor | Source | Analysis |
|---|-------------|--------|----------|
| 1 | CPU vs GPU threshold | sc-best-practices.org | Below ~50k cells: CPU scanpy is fine; GPU transfer overhead dominates |
| 2 | GPU sweet spot | sc-best-practices.org | 50k–1M cells on one GPU is optimal; >1M requires distributed computing |
| 3 | Pre-trained vs scratch | bioRxiv:2025.04.14.648850 | Pre-trained foundation models (scGPT, Geneformer) outperform task-specific models; fine-tuning is cost-effective |
| 4 | Sparse vs dense | sc-best-practices.org | Sparse CSR is essential; dense representations OOM on large datasets |
| 5 | Random vs sequential I/O | arXiv:2506.01883 | True random sampling: ~20 samples/sec on Tahoe-100M (58 days/epoch); scDataset: 100× speedup |
| 6 | Cloud GPU costs | Caltech HPC | H100 nodes: 16+ available; V100: 8 nodes; P100: 200 nodes |

---

## 7. Single-Cell ML Scalability

| # | Scalability Challenge | Source | Limit |
|---|----------------------|--------|-------|
| 1 | VRAM bottleneck | sc-best-practices.org | 1M cells × 30k genes dense = ~120 GB; sparse CSR required |
| 2 | I/O bottleneck | arXiv:2506.01883 | Tahoe-100M: 314 GB sparse; >1 TB decompressed; random access = 58 days/epoch |
| 3 | KNN scaling | sc-best-practices.org | Exact KNN scales O(n²); ANN backend needed above ~500k cells |
| 4 | Foundation model scaling | bioRxiv:2025.04.14.648850 | C2S-Scale: 410M–27B parameters; 1B+ token corpus; 50M+ cells |
| 5 | Multi-GPU execution | sc-best-practices.org | dask-cuda for out-of-core; synchronization points at QC, HVG, scaling, PCA |
| 6 | Data loading | arXiv:2506.01883 | scDataset achieves quasi-random sampling with 100× speedup over true random |

---

## 8. Single-Cell ML Biosecurity & Dual-Use

| # | Concern | Source | Details |
|---|---------|--------|---------|
| 1 | Generative AI dual-use | arXiv:2510.15975 | GenAI lowers barrier to misuse; can generate synthetic viral proteins or toxins; jailbreak vulnerabilities |
| 2 | Upstream risk-benefit review | Frontiers in Microbiology 2026 | Current BAIM governance focuses on post-development; upstream pre-development RBR is missing |
| 3 | Biological AI model capabilities | PMC12061118 | LLMs (GPT-4, 4o) show rapid progress in dual-use capabilities; protein design models vulnerable to misuse |
| 4 | Governance frameworks | arXiv:2510.15975 | 74% of 130 experts called for new governance frameworks; multi-layered defense advocated |
| 5 | Mitigation strategies | arXiv:2510.15975 | Data filtering, alignment with ethical principles, real-time monitoring to block harmful requests |

---

## 9. Single-Cell ML Failure Modes

| # | Failure Mode | Source | Description |
|---|-------------|--------|-------------|
| 1 | Batch effects dominate embeddings | PMC12007350 | Geneformer and scGPT fail to correct batch effects between techniques; clustering driven by batch not cell type |
| 2 | Zero-shot limitations | PMC12007350 | Foundation models perform poorly on unseen datasets; unclear relationship between pretraining objective and clustering |
| 3 | Gene-level batch effects | PubMed:40579473 | As few as 3 highly batch-sensitive genes (HBGs) introduce substantial batch effects |
| 4 | Overcorrection | PMC8494213 | Scanorama largely fails to correct batch effects; DCA underperforms vs CarDEC and scVI |
| 5 | Pretraining objective mismatch | PMC12007350 | Models perform poorly on datasets seen during pretraining; batch labels not used in scGPT/Geneformer pretraining |
| 6 | Dropout and sparsity | PMC8769926 | High sparsity requires imputation; DeepImpute, MAGIC, DCA, scImpute address but with tradeoffs |

---

## 10. scGPT: Foundation Model for Single-Cell Multi-Omics

| Attribute | Details |
|-----------|---------|
| **Architecture** | 53M parameter transformer, 12 stacked blocks, 8 attention heads, embedding dim 512 |
| **Pretraining Data** | 33 million normal human cells from CELLxGENE Discover corpus |
| **Key Innovation** | Masked multi-head attention for unordered gene sets; joint cell and gene embeddings |
| **Input Tokens** | Gene identity tokens + binned expression value tokens + condition tokens (batch, perturbation, modality) |
| **Pretraining Objective** | Two-step masked gene expression prediction: predict masked genes + global cell embedding, then refine |
| **Downstream Tasks** | Cell type annotation, multi-batch integration, multi-omic integration (scATAC-seq), perturbation prediction, gene network inference |
| **Scaling Law** | Larger pretraining data → superior embeddings → improved downstream performance |
| **Variants** | Whole-human (33M cells), brain (13.2M cells), blood/bone marrow (10.3M cells) |
| **Limitations** | Fails to correct batch effects between techniques; zero-shot performance limited; batch labels not used in pretraining |
| **Code** | https://github.com/bowang-lab/scGPT |
| **Citation** | Wang et al., Nature Methods, February 2024 |

---

## Bottlenecks Summary

1. **Batch effects**: Technical and biological variation dominates embeddings; foundation models (scGPT, Geneformer) fail to correct cross-technique batch effects
2. **VRAM limitations**: 1M cells × 30k genes = ~120 GB dense; sparse representations mandatory
3. **I/O bottleneck**: On-disk data loading is prohibitive; random access patterns yield ~20 samples/sec on 100M-cell datasets
4. **Scalability**: Exact KNN scales O(n²); ANN required above ~500k cells; multi-GPU needed above 1M cells
5. **Interpretability**: Deep learning models lack transparency; attention weights and gradient-based methods provide post-hoc explanations
6. **Zero-shot limitations**: Foundation models perform poorly on unseen datasets; pretraining objective mismatch
7. **Data integration**: Multimodal integration lacks ground truth for evaluation; embedding quality is ill-posed
8. **Computational cost**: Training foundation models (C2S-Scale 27B) requires massive compute; fine-tuning is cost-effective alternative
9. **Dropout/sparsity**: High dropout rates in scRNA-seq require imputation; tradeoffs between accuracy and computational cost
10. **Biosecurity**: Generative AI dual-use risks; jailbreak vulnerabilities; need for upstream governance

---

## Citations

1. Yiu T, Chen B, Wang H, et al. Transformative advances in single-cell omics: comprehensive review of foundation models, multimodal integration and computational ecosystems. PMC12560279.
2. Sasaki D, Kashiwazaki H, Osaki M, et al. Review of Machine Learning Advancements for Single-Cell Analysis. COMPSAC 2023. DOI:10.1109/COMPSAC57700.2023.00210.
3. Li H, Xu H. Novel Machine Learning Framework for Single-Cell Analysis. JMLR 2025.
4. Deep Learning in Single-Cell Analysis. arXiv:2210.12385.
5. Deep Learning in Single-cell Analysis. ACM Transactions on Intelligent Systems and Technology. DOI:10.1145/3641284.
6. Baek S, et al. Single-cell foundation models: bringing artificial intelligence into cell biology. PubMed:41028523.
7. Applications of AI to single-cell and spatial transcriptomics. PMC12886477.
8. Single-Cell Omics Deep Learning. Emergent Mind, 2026.
9. Towards Label-Free Single-Cell Phenotyping Using Multi-Task Learning. arXiv:2605.14717.
10. Single-Cell Toolkit. Multiome Academy.
11. mLLMCelltype: Multi-LLM Consensus Framework for Cell Type Annotation. GitHub:cafferychen777/mLLMCelltype.
12. Bio Open Science Index. index.bio.xyz.
13. GPU-accelerated analysis — Single-cell best practices. sc-best-practices.org.
14. GPU Computing — Caltech Resnick HPC Center.
15. Deep learning tackles single-cell analysis. PMC8769926.
16. Single-Cell Analysis Using Machine Learning Techniques. PMC8614827.
17. Scaling Large Language Models for Next-Generation Single-Cell Analysis. bioRxiv:2025.04.14.648850.
18. scDataset: Scalable Data Loading for Deep Learning on Large-Scale Single-Cell Omics. arXiv:2506.01883.
19. Generative AI for Biosciences: Emerging Threats and Roadmap to Biosecurity. arXiv:2510.15975.
20. Dual-use artificial intelligence and biology: upstream risk-benefit reviews. Frontiers in Microbiology 2026.
21. Dual-use capabilities of concern of biological AI models. PMC12061118.
22. Quantifying batch effects for individual genes in single-cell data. Nat Comput Sci. 2025;5(8):612-620.
23. Zero-shot evaluation reveals limitations of single-cell foundation models. PMC12007350.
24. A joint deep learning model enables simultaneous batch effect correction, denoising, and clustering. PMC8494213.
25. Wang B, et al. scGPT: Towards Building a Foundation Model for Single-Cell Multi-Omics Using Generative AI. bioRxiv:2023.04.30.538439.
