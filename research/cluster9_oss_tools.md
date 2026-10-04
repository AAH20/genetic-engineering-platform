# Cluster 9: AI/ML for Genomics — OSS Tools Research

**Date:** 2026-10-04
**Search queries:** 10 parallel web searches, top 3 results each

---

## 1. OSS Projects

| Project | Description | License | URL |
|---------|-------------|---------|-----|
| DeepVariant | CNN-based variant caller (Google/Verily); treats variant calling as image classification | Open Source | github.com/google/deepvariant |
| Clair3 | Deep learning variant caller for long-read (ONT) data | Open Source | github.com/HKU-BAL/Clair3 |
| PEPPER-Margin-DeepVariant | Combined ONT pipeline: PEPPER (candidate discovery) + Margin (haplotype polishing) + DeepVariant | Open Source | github.com/kishwarshafin/pepper |
| NVIDIA Parabricks | GPU-accelerated GATK/DeepVariant for high-throughput environments | Commercial (GPU) | nvidia.com/clara |
| GATK (Broad Institute) | Industry-standard variant discovery toolkit with ML components | Free (some commercial) | github.com/broadinstitute/gatk |
| DeepChem | Python library for scientific ML; now includes DeepChem-Variant for genomics | Open Source (MIT) | github.com/deepchem/deepchem |
| scVI | Variational autoencoder for single-cell dimensionality reduction & batch correction | Open Source | github.com/scverse/scvi-tools |
| MOFA+ | Matrix factorization for multi-omics data integration | Open Source | github.com/bioFAM/MOFA2 |
| Nucleotide Transformer | Transformer-based DNA sequence representation learning | Open Source | github.com/instadeepai/nucleotide-transformer |
| Carbon (HuggingFace) | Autoregressive DNA foundation model (500M/3B/8B); 6-mer tokenization; Apache 2.0 | Open Source | huggingface.co/Carbon-8B |
| ModernGENA | Modernized BERT-style backbone for DNA; efficient baseline for genomic language models | Open Source | huggingface.co (DNA LM collection) |
| DaisyChain Genomics | Modular genomic model: 4×74M specialists + learned router; ~7× cheaper inference than monolith | Open Source | huggingface.co/DaisyChainAI/daisychain-genomics |
| EUGENe (ML4GLand) | Python toolkit for sequence activity prediction and analysis | Open Source | github.com/ML4GLand/EUGENe |
| SeqPro (ML4GLand) | Genomic sequence preprocessing toolkit | Open Source | github.com/ML4GLand/SeqPro |
| GenomeSpy | GPU-accelerated visualization grammar for genomic data | MIT | github.com/genome-spy/genome-spy |
| Embarrassingly_FASTA | GPU-accelerated preprocessing pipeline (Parabricks-based); $120→<$1/genome | Open Source | biorxiv.org/10.64898/2026.02.02.703356 |
| CompoSeq | Composable primitives for genomic analysis; SQL dialect for interval operations | Open Source | composeq.dev |
| DeepConsensus | PacBio HiFi polishing via deep learning | Open Source | github.com/google/deepconsensus |
| GenoML | Automated ML platform for genomics data analysis | Commercial | genoml.com |

---

## 2. SOTA Approaches

- **Variant calling:** DeepVariant (CNN image classification) remains gold standard for accuracy; Clair3 for long reads; PEPPER-Margin-DV for ONT best-in-class F1
- **Foundation models:** Carbon-8B matches Evo2-7B win rates at ~275× throughput via 6-mer tokenization; scores full human genome on single GPU in <2 days
- **Single-cell analysis:** scVI (variational autoencoder) for dimensionality reduction, batch correction, differential expression in one model
- **Multi-omics integration:** MOFA+ (matrix factorization) and graph-based methods
- **Efficient architectures:** ModernGENA (ModernBERT-style) achieves strong efficiency-quality trade-off; DaisyChain uses mixture-of-specialists routing for 7× cheaper inference
- **GPU acceleration:** Embarrassingly_FASTA achieves 25-30× speedup over CPU; 35 min/genome vs 15+ hours
- **DeepChem-Variant:** Modular CNN (InceptionV3/MobileNetV2) for variant calling within DeepChem framework

---

## 3. Bottlenecks

- **Data quality & heterogeneity:** Lack of DL-based published protocols for new, heterogeneous datasets requiring significant data engineering
- **Foundation model complexity:** Quadratic computational complexity (O(n²)) in self-attention limits long-range genomic modeling
- **GNN scalability:** Over-smoothing and neighbor explosion when applied to large-scale biological networks
- **Tool fragmentation:** Most bioinformatics code dedicated to I/O; intermediate file copies at every step; tightly coupled to specific formats
- **Small sample sizes:** Over-parameterized DL models overfit in low-sample regimes; traditional methods (PCA, HMM, DESeq2) remain advantageous
- **Population bias:** Training data lacks diversity; performance degrades substantially outside training distribution
- **Interpretability:** Black-box models limit clinical adoption; need for causal inference and explainable AI
- **Computational cost:** Population-scale reprocessing impractical; 15+ hours per genome on CPU
- **Integration gap:** ML/AI application to clinical genomic translation remains largely untapped

---

## 4. Hardware Requirements

- **GPU acceleration essential:** DL models require GPUs for practical runtimes; NVIDIA V100, A100, H100, H200 common
- **Cloud GPU pricing:** H100 ~$2.50-3.20/GPU-hour; H200/B200 ~$4.00-5.50/GPU-hour (on-demand, early 2026)
- **Spot instances:** 30-50% discount; Embarrassingly_FASTA leverages spot for <$1/genome
- **Typical cluster:** 8×A10 GPUs process 30× WGS in ~35 min; CPU equivalent: 96-vCPU instance, 15+ hours
- **Memory:** High-memory nodes needed for large genome processing; 2PB+ storage for population-scale
- **FPGA/GPU hybrid:** Illumina DRAGEN uses hardware acceleration for clinical-grade speed
- **MIG support:** NVIDIA Multi-Instance GPU for better utilization in shared environments

---

## 5. Cost Tradeoffs

| Approach | Cost | Notes |
|----------|------|-------|
| CPU pipeline (GATK) | ~$17-120/genome | 15+ hours; commercial secondary analysis ~$120 |
| GPU pipeline (Parabricks) | <$1-2/genome | 35 min; 18× cheaper than CPU |
| Cloud SaaS (AI target validation) | $45K-310K/year | Median $310K for mid-sized biotech |
| Enterprise AI platform | $500K-5M/year | Schrödinger, Atomwise, BenevolentAI |
| Traditional wet-lab validation | $250K-400K/target | 14-18 months |
| AI platform validation | $3K-15K/target | 4-6 weeks |
| Clinical genomics platform build | $750K-1.5M | AI/ML layer = 40-60% of cost |
| Annual maintenance | 15-25% of build cost | Compliance, revalidation, scaling |

**ROI:** 3-7× over 3-5 year horizon; break-even at ~12 targets/year (SaaS) to 40 targets/year (enterprise)

---

## 6. Scalability Limits

- **Quadratic attention:** Foundation models face O(n²) complexity; Carbon-8B reaches ~786 kbp via YaRN extrapolation
- **Population-scale storage:** Current repositories ~tens of petabytes; need exabyte-scale for tens of millions of individuals
- **Compute at scale:** Nation-sized cohorts = billions in compute; years of aggregate CPU time
- **I/O bottleneck:** Most time wasted routing data through tools creating intermediate copies
- **CompoSeq solution:** Make genomic data operate natively within modern analytics/ML systems; SQL dialect transpiling across engines
- **Embarrassingly_FASTA:** Transient intermediate lifecycle + spot-friendly orchestration enables recomputable pangenomics
- **Whole Genome Models (WGMs):** Population-scale foundation models trained over millions of genomes; require fundamental infrastructure expansion

---

## 7. Biosecurity Governance

- **Dual-use risk:** Deep generative models can predict novel biological molecules not resembling existing sequences; could bypass nucleic acid synthesis screening
- **Database matching vulnerability:** Current screening relies on database matching; AI-generated sequences may evade detection
- **Nature Biotechnology call (2025):** Wang et al. call for built-in biosecurity safeguards for generative AI tools
- **NHGRI ELSI framework:** Consortium-agreed-upon ELSI framework for ML/AI tool integration into clinical decision-making
- **ELSI recommendations:** Partnerships between ELSI researchers, tool developers, genomic researchers; regulatory body for standards
- **Bias amplification:** Need methods to evaluate algorithms for unintended consequences (e.g., amplifying biases)
- **Synthetic biology risk:** AI science agents could automate experimental designs for pathogen engineering
- **Governance gap:** No unified regulatory framework; FDA guidance on AI/ML-enabled drug development tools (March 2026) adds compliance requirements

---

## 8. Failure Modes

- **Overfitting in small cohorts:** DL models overfit when training data is limited; traditional statistical methods outperform
- **Distribution shift:** Performance degrades substantially outside training population/species
- **False positives in validation:** 7-13% false-positive rate even for best models (AUC 0.87-0.93); skipping orthogonal validation leads to wasted resources
- **Tool fragmentation:** Brittle, format-coupled tools create maintenance burden and limit agent usability
- **Data preparation gaps:** Raw FASTQ/mzML requires significant preprocessing; vendor pipelines optimized for speed over sensitivity
- **Interpretability failure:** Black-box predictions without mechanistic understanding limit clinical trust
- **Cost underestimation:** Hidden costs: data harmonization ($10-30K), user training (15-20% of contract), compliance packages ($25-180K/year)

---

## 9. NP-Hard Problems

- **Multi-omics integration:** Remains one of computational biology's hardest problems; matrix factorization and graph-based methods making progress but no general solution
- **Variant calling in repetitive regions:** Long-read technologies help but structural variant detection in complex regions remains challenging
- **Protein folding:** AlphaFold-class models solved prediction but design (inverse folding) remains difficult
- **Regulatory grammar:** Capturing long-range genomic dependencies (>100 kb) with quadratic attention is computationally prohibitive
- **Pangenome construction:** Population-scale pangenome build-up requires exabyte-scale storage and compute
- **Causal inference:** ML models predict but cannot infer causality; integration of causal frameworks with predictive models is an open problem

---

## 10. Most Cited Papers

1. **Poplin et al. (2018)** — DeepVariant: Creating a universal variant caller with deep learning. *Nature Biotechnology*
2. **Ramsundar et al. (2019)** — DeepChem: Democratizing deep-learning for drug discovery. *Journal of Chemical Information and Modeling*
3. **Wang et al. (2025)** — A call for built-in biosecurity safeguards for generative AI tools. *Nature Biotechnology* 43:845-847
4. **Zou et al. (2019)** — A primer on deep learning in genomics. *Nature Genetics*
5. **Eraslan et al. (2019)** — Single-cell RNA-seq denoising using a deep count autoencoder. *Nature Communications*
6. **Avsec et al. (2025)** — Whole Genome Models (WGMs): Population-scale genomic foundation models
7. **Brixi et al. (2025)** — Genomic foundation model scaling
8. **Dalla-Torre et al. (2025)** — Genomic language model advances
9. **Feng et al. (2025)** — Population-scale genomics with ML
10. **Koreniuk & Njie (2025)** — Efficient genomic model architectures

---

## 11. Integration Challenges

- **Format fragmentation:** Tight coupling to specific file formats (BAM, VCF, FASTQ); most code dedicated to parsing/I/O
- **Tool chaining:** Intermediate copies at every step; ad hoc scripts for edge cases
- **Data heterogeneity:** Multimodal datasets (genomics, multi-omics, phenotypic, SDOH, EHR, IoT) require unified representations
- **FAIR data principles:** Interoperability standards and data sharing policies needed for effective ML training
- **Clinical validation:** Tools must mimic realistic clinical decision-making scenarios; cross-validation across sites
- **ELSI integration:** Ethical, legal, social implications must be embedded in tool development, not bolted on
- **CompoSeq paradigm:** Flip from format-coupled tools to composable primitives operating natively in modern analytics/ML systems
- **NHGRI consortium model:** 3-4 tool development sites + Coordinating Center; $30M over 5 years for ML/AI tool development and validation

---

## Citations

1. Poplin, R. et al. DeepVariant: Creating a universal variant caller with deep learning. *Nature Biotechnology* (2018).
2. Wang, M. et al. A call for built-in biosecurity safeguards for generative AI tools. *Nature Biotechnology* 43, 845-847 (2025). doi:10.1038/s41587-025-02650-8
3. NHGRI. ML/AI Tools to Advance Genomic Translational Research. Concept Clearance (2023).
4. NHGRI. Machine Learning In Genomics Workshop: Executive Summary (2021).
5. Zou, J. et al. A primer on deep learning in genomics. *Nature Genetics* (2019).
6. Eraslan, G. et al. Single-cell RNA-seq denoising using a deep count autoencoder. *Nature Communications* (2019).
7. Ramsundar, B. et al. DeepChem: Democratizing deep-learning for drug discovery. *J. Chem. Inf. Model.* (2019).
8. Embarrassingly_FASTA: Enabling Recomputable, Population-Scale Pangenomics. *bioRxiv* (2026). doi:10.64898/2026.02.02.703356
9. ModernGENA: ModernBERT for DNA Foundation Models. *bioRxiv* (2026). doi:10.64898/2026.04.21.719816
10. Carbon: DNA & Gene Model. HuggingFace / Zhongguancun Academy / TIGEM (2026).
11. DaisyChain Genomics. HuggingFace / DaisyChainAI (2026).
12. CompoSeq: Composable Primitives for Genomic Analysis. NECB 2026 Abstract A057.
13. Illumina Releases Open Source AI Software. Illumina (2018).
14. Genomics in the Machine Learning Space. NHGRI Presentation (E. Topol).
15. AI and Machine Learning for Genomics: From Sequence Analysis to Biological Insight. *Technology Networks* (2024).
