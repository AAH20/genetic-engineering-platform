# Cluster 9: Genomic Foundation Models (GFMs)

## Overview

Genomic foundation models (GFMs) are large-scale neural networks pretrained on massive unlabeled DNA sequence corpora, adapted to downstream tasks such as regulatory element prediction, variant effect scoring, and genome annotation. The field has rapidly evolved from early k-mer-based transformers (DNABERT, 2021) to billion-parameter models with genome-scale context windows (Evo 2, 40B parameters, 1M+ context). This review synthesizes 10 research dimensions including architecture, scalability, cost, biosecurity, and fundamental limitations.

---

## 1. State-of-the-Art Approaches

### Leading Models

| Model | Params | Context | Architecture | Training Data | Key Innovation |
|-------|--------|---------|-------------|---------------|----------------|
| **Evo 2** | 7B / 40B | 1 Mb | StripedHyena2 (hybrid SSM) | 9.3T nucleotides, 128K+ genomes across all domains of life | Scaling laws on DNA; zero-shot function prediction across DNA/RNA/protein |
| **Nucleotide Transformer v2** | 50M–2.5B | 6–12 Kb | Transformer (BERT/RoFormer) | 3,202 human + 850 multi-species genomes | Multi-species pretraining; 11/18 zero-shot task parity |
| **HyenaDNA** | 1M–1B | 1M tokens | Hyena (subquadratic operators) | Human reference genome | Single-nucleotide resolution at 1M context |
| **DNABERT-2** | 117M | Variable | Transformer + BPE + ALiBi | Multi-species genomes | BPE replaces k-mer; 21× fewer params, 92× less GPU time than NT |
| **dnaHNet** | 10M–1B | Variable | H-Net (tokenizer-free, hierarchical) | Prokaryotic genomes (GTDB) | Differentiable dynamic chunking; >3× inference speedup over Transformers |
| **GENERator-v2** | 0.5–3B | 98 Kb | Transformer decoder + 6-mer | 386B nucleotides eukaryotic DNA | Factorized Nucleotide Supervision (FNS) + Genome Compression Pretraining (GCP) |
| **SUCCEED** | — | 131 Kb | Convolutional + Transformer | 6,389 ENCODE functional genomics tracks | Supervised multi-task; transferable regulatory representations |
| **METAGENE-1** | 7B | 512 tokens | Llama 2 | 1.5T base pairs wastewater metagenomic | Pathogen detection from metagenomic sequences |
| **Genos (BGI)** | 1.2B / 10B | 1M bp | Mixture of Experts (MoE) | Human-centric | Clinical human genome optimization |

### Key Architectural Trends

- **Tokenization evolution**: k-mer → BPE → byte-level → tokenizer-free (dnaHNet). Fixed-vocabulary tokenizers fragment biologically meaningful motifs (codons, regulatory elements), while nucleotide-level models preserve biological coherence at prohibitive computational cost.
- **Long-context architectures**: StripedHyena (hybrid attention + data-controlled convolutions), Hyena operators (subquadratic), and hierarchical compression (H-Net) enable genome-scale context without quadratic attention cost.
- **Training objectives**: Autoregressive next-token prediction (Evo, Evo 2), masked language modeling (NT, DNABERT-2), and supervised multi-task learning (SUCCEED) represent the three dominant paradigms.

---

## 2. Bottlenecks

1. **Entropy-induced representation instability**: Genomic sequences have fundamentally higher conditional entropy than text, producing near-uniform output distributions (KL divergence to uniform ~3 bits for BPE models vs >10 bits for text), ensemble disagreement, and unstable static embeddings even under matched architecture/training/data [1].

2. **Tokenization bottleneck**: Fixed-vocabulary tokenizers fragment biologically meaningful motifs; nucleotide-level models preserve coherence but incur prohibitive computational costs for long contexts. The bilevel optimization of quality-aware tokenization is NP-hard [2].

3. **Geometric Alignment Tax**: Forcing continuous biological manifolds through discrete categorical bottlenecks introduces intrinsic distortion. Under discrete tokenization, architectures diverge by 3,000× on biological mutation walks vs 1.3× under continuous objectives [3].

4. **Data sparsity in eukaryotic genomes**: Functional signal is extremely sparse along eukaryotic genomes, making long-context modeling inefficient without explicit data construction strategies like Genome Compression Pretraining [4].

5. **Inter-token relationship underutilization**: Fisher information analysis shows DNA models concentrate information in embedding layers rather than transformer layers, failing to exploit inter-token relationships [1].

6. **Scalability-efficiency tension**: Standard Transformers face quadratic attention costs at single-nucleotide resolution; subquadratic alternatives (Hyena, StripedHyena) improve scaling but may sacrifice biological fidelity.

---

## 3. NP-Hard Problems

1. **Quality-Aware Tokenization (QA-Token)**: Formalized as a bilevel optimization problem jointly optimizing vocabulary construction and downstream performance. Proven NP-hard (Theorem 3.2); polynomial bilevel programming is Σ₂P-hard, placing it one level above NP in the polynomial hierarchy. Worst case requires exponential evaluations [2].

2. **Optimal tokenizer-free compression**: dnaHNet's differentiable dynamic chunking learns compression ratios adaptively, but finding the globally optimal compression schedule is computationally intractable, requiring greedy approximation schemes [5].

3. **Genome Compression Pretraining (GCP)**: Selecting optimal gene-centric and regulatory regions for concatenation while discarding low-information background is a combinatorial optimization problem without known polynomial-time solution [4].

---

## 4. Algorithms

### Core Algorithmic Innovations

- **StripedHyena**: Hybridizes attention with data-controlled convolutional operators for near-linear compute scaling relative to sequence length. Powers Evo (7B) and Evo 2 (40B) [6].
- **Hyena operators**: Subquadratic drop-in replacement for attention enabling 1M token context at single-nucleotide resolution [7].
- **H-Net hierarchical compression**: Recursive differentiable chunking with encoder-decoder architecture. Allocates ~30% parameters to encoder-decoder (vs 15% for text) to capture complex genomic local dependencies [5].
- **Factorized Nucleotide Supervision (FNS)**: Reinterprets k-mer tokens as structured objects; derives nucleotide-level conditional probabilities from same logits without modifying architecture [4].
- **Genome Compression Pretraining (GCP)**: Data construction strategy concentrating on gene-centric/regulatory regions, implementing sparse-attention-like effects at the data level [4].
- **Spectral deformation locking**: Weight-locking method to prevent fine-tuning of open-weight GFMs on pathogen data. Defeats naive fine-tuning and LoRA attacks [8].
- **Cost-Aware Prompt Tuning (CAPT)**: Jointly optimizes prompt-tuning objective with hierarchical cloud-cost model (per-GPU-hour, egress, storage) [9].

---

## 5. Open-Source Projects

| Project | License | Description |
|---------|---------|-------------|
| [Evo 2 (Arc Institute)](https://huggingface.co/arcinstitute/evo2_7b) | Apache 2.0 | 7B/40B GFM trained on OpenGenome2 (8.8T bases), all domains of life |
| [Nucleotide Transformer v2 (InstaDeepAI)](https://huggingface.co/InstaDeepAI/nucleotide-transformer-v2-500m-multi-species) | Apache 2.0 | 50M–2.5B multi-species DNA foundation models |
| [DNABERT-2](https://huggingface.co/zhihan1996/DNABERT-2-117M) | Apache 2.0 | 117M efficient multi-species genome model (ICLR 2024) |
| [HyenaDNA (LongSafari)](https://huggingface.co/LongSafari) | — | 1M context long-context GFM (Stanford/Harvard) |
| [scGPT (bowang-lab)](https://github.com/bowang-lab/scGPT) | — | Single-cell foundation model, 33M+ cells |
| [GeneCompass (xCompass-AI)](https://github.com/yikunpku/RNA-MSM) | MIT | Cross-species knowledge-informed model, 120M+ single-cell transcriptomes |
| [Plant-BERT (nigelhartm)](https://huggingface.co/nigelhartm) | — | BERT-based plant genome model |
| [OpenGenomeLLM](https://opengenomellm.org/models.html) | — | Catalog of foundation DNA models with benchmarks |
| [genomic-foundation-models (mtariqi)](https://github.com/mtariqi/genomic-foundation-models) | — | Production-quality PyTorch: pre-training, single-cell classification, variant effect prediction |
| [Goodfire Evo-2 SAE](https://huggingface.co/Goodfire/Evo-2-Layer-26-Mixed) | — | Sparse autoencoder for Evo 2 interpretability (32,768-dim sparse latent) |

---

## 6. Hardware Requirements

### Training

- **Evo 2 (7B/40B)**: Requires multi-GPU training infrastructure; trained on 9.3T nucleotides across 128K+ genomes [6].
- **Nucleotide Transformer (2.5B)**: Trained on 3,202 human + 850 multi-species genomes; requires substantial GPU clusters [10].
- **METAGENE-1 (7B)**: Trained on 1.5T base pairs of wastewater metagenomic sequences [11].

### Inference

- **Minimum GPU memory**: ~3× billion parameters in GB (e.g., 12B model → 36GB minimum) [12].
- **NVIDIA NIM for GenMol**: Supports single-GPU inference on RTX 6000 Ada (48GB), L40S (48GB), A100 (40/80GB), H100 (80GB), H200 (141GB), B200 (180GB), GB200 (186GB) [13].
- **Benchmarking study**: NT, Evo2, HyenaDNA, DNABERT2 benchmarked on single NVIDIA H100 (96GB VRAM), 128GB system RAM [14].
- **Resource-constrained settings**: GERM enables fine-tuning via QLoRA and quantization (OmniQuant) on consumer hardware [15].

---

## 7. Cost Analysis

### Training Costs

- **Single-cell foundation models**: Initial training/fine-tuning typically $12,000–$40,000 in compute credits depending on dataset size and architecture [16].
- **Fine-tuning per project**: $8,000–$25,000 in compute credits; transfer learning reduces baseline by 40–60% [16].

### Inference Costs

- **Per-sequence inference**: $0.001–$0.005 per cellular profile for pre-trained embeddings [16].
- **Full fine-tuning**: $0.030 ± $0.004 per sequence (synthetic baseline) [9].
- **Prompt tuning**: $0.021 ± $0.003 per sequence [9].
- **Cost-Aware Prompt Tuning (CAPT)**: $0.015 ± $0.001 per sequence — 50% reduction vs full fine-tuning, 28.6% vs prompt tuning [9].
- **Quantized inference**: $0.012 ± $0.002 per sequence [9].

### Cloud Pricing (per GPU-hour)

| Provider | GPU | Price (USD/hr) |
|----------|-----|----------------|
| AWS | p2.xlarge | $0.90 |
| GCP | nvidia-v100 | $1.21 |
| Azure | NC6 | $1.10 |

### Cost Optimization Strategies

- **GERM**: Outlier removal improves fine-tuning performance by 37.98% and quantization by 64.34%, reducing computational demands [15].
- **DNABERT-2**: 21× fewer parameters, 92× less pretraining GPU time than Nucleotide Transformer [17].
- **dnaHNet**: >3× inference speedup over Transformers via quadratic FLOP reduction [5].

---

## 8. Scalability Limits

### Context Length vs. Compute

- **Standard Transformers**: Quadratic attention cost limits practical context to ~12–24 Kb at single-nucleotide resolution.
- **HyenaDNA**: 1M token context via subquadratic operators, but may sacrifice some biological fidelity.
- **Evo 2**: 1 Mb context via StripedHyena2 hybrid architecture with near-linear scaling.
- **dnaHNet**: Hierarchical compression yields quadratic FLOP reductions, enabling efficient long-context modeling.

### Scaling Laws

- **Evo**: Demonstrated scaling laws on DNA complementing observations in NLP and vision. Performance improves predictably with model size and training data [6].
- **dnaHNet**: Outperforms StripedHyena2 in scaling and efficiency; recursive compression enables superior scaling behavior [5].

### Fundamental Scalability Constraints

1. **Entropy ceiling**: High conditional entropy of genomic sequences limits the effectiveness of self-supervised training regardless of model scale [1].
2. **Geometric distortion**: Discrete tokenization imposes a fundamental tax on representation quality that worsens with finer quantization [3].
3. **Data availability**: Training corpora are limited by available sequenced genomes; eukaryotic genomes are particularly sparse in functional annotation.

---

## 9. Biosecurity & Governance

### Dual-Use Risks

- **Open-weight GFMs**: Models like Evo 2 (Apache 2.0) can be fine-tuned on pathogen data to recover virological capabilities. With 25,000 gradient steps on a modest pathogen corpus, an unlocked Evo improves held-out viral perplexity from 3.729 to 3.487 [8].
- **Adversarial evasion**: GFMs (DNABERT-2, NT v2) are vulnerable to perturbation-efficient adversarial attacks requiring only a few nucleotide edits. Effective substitutions favor transversions and concentrate in 5' regulatory regions. Iterative adversarial training reduces attack success from ~40–45% to ~20–30% [18].
- **Training data filtering insufficient**: Excluding human-infecting viral genomes from pretraining corpora is easily circumvented by fine-tuning on abundantly available viral data [8].

### Defensive Applications

- **AMR detection**: Evo 2 embeddings + probing + sparse autoencoders enable accurate identification of antimicrobial resistance signals from metagenomic data, including MAG-derived sequences and simulated reads [11].
- **Biosecurity screening**: Embedding-based representations provide scalable framework for resistome profiling and detection of engineered resistance elements [11].

### Governance Mechanisms

- **Spectral deformation locking**: Weight-locking technique that prevents fine-tuning on pathogen data. Defeats naive fine-tuning and LoRA; informed attackers using SVD-chain construction can recover capability at increased computational cost [8].
- **Adversarial training**: Reduces but does not eliminate attack success rates [18].
- **Responsible release**: Evo excluded viral genomes that infect eukaryotic hosts from training data [6].

---

## 10. Failure Modes

### Representation Failures

1. **Near-uniform output distributions**: High genomic entropy produces flat predictive distributions (KL to uniform ~3 bits for BPE, <1 bit for k-mer, vs >10 bits for text), precluding high-confidence predictions [1].

2. **Ensemble disagreement**: Models matched in architecture, training, and data produce divergent predictions, revealing deep output instability [1].

3. **Unstable embeddings**: Embedding spaces are non-robust with respect to initialization; interpretability and reproducibility within and across training runs are compromised [1].

4. **Geometric Alignment Tax**: Three failure regimes identified across 14 biological foundation models:
   - **Local-Global Decoupling**: Models encode shallow local statistics but fail to integrate globally.
   - **Representational Compression**: Information concentrators amplify mutual information at cost of geometric fidelity.
   - **Geometric Vacuity**: Smooth embeddings carry less structure than random noise [3].

5. **Brittle Glass vs. Untethered Glass**: ESM-2 protein models show progressive decline in geometric stability with scale (Brittle Glass: ρ < 2%; Untethered Gel: ρ > 4%) [3].

### Training Failures

6. **Self-supervised training insufficiency**: Evidence suggests self-supervised training from sequences alone may not be applicable to genomic data, calling into question assumptions underlying current GFM methodologies [1].

7. **Fisher information concentration**: DNA models concentrate Fisher information in embedding layers, failing to exploit inter-token relationships in transformer layers [1].

8. **Reverse-complement robustness illusion**: Evo 2's apparent reverse-complement robustness reflects conserved sequence composition, not learned symmetry [3].

### Deployment Failures

9. **Adversarial vulnerability**: GFMs remain vulnerable to biologically constrained adversarial attacks even after adversarial training [18].

10. **Fine-tuning misuse**: Open-weight models can be fine-tuned to recover pathogen capabilities despite training data filtering [8].

---

## Citations

[1] "Entropy, Disagreement, and the Limits of Foundation Models in Genomics." arXiv:2604.04287. https://arxiv.org/pdf/2604.04287v1

[2] "Unlocking Noisy Real-World Corpora for Foundation Model Pre-Training via Quality-Aware Tokenization." arXiv:2602.06394. https://arxiv.org/html/2602.06394v1

[3] "The Geometric Alignment Tax: Tokenization vs. Continuous Geometry in Scientific Foundation Models." arXiv:2604.04155. https://arxiv.org/pdf/2604.04155v1.pdf

[4] "Functional In-Context Learning in Genomic Language Models with Nucleotide-Level Supervision and Genome Compression." bioRxiv:2026.01.27.702015. https://biorxiv.org/content/10.64898/2026.01.27.702015v1.full-text

[5] "dnaHNet: A Scalable and Hierarchical Foundation Model for Genomic Sequence Learning." arXiv:2602.10603. https://arxiv.org/pdf/2602.10603.pdf

[6] "Sequence modeling and design from molecular to genome scale with Evo." Science, 2024. https://pmc.ncbi.nlm.nih.gov/articles/PMC12057570

[7] "HyenaDNA: Long-Range Genomic Sequence Modeling at Single Nucleotide Resolution." Stanford/Harvard, 2023.

[8] "Spectral Deformation Locking of Genomic Foundation Models." bioRxiv:2026.07.07.736795. https://biorxiv.org/content/10.64898/2026.07.07.736795v1.full.pdf

[9] "Cost-Aware Prompt Tuning for Genomic Foundation Models on Multi-Cloud Platforms." https://freederia.com/cost-aware-prompt-tuning-for-genomic-foundation-models-on-multi-cloud-platforms

[10] "The Nucleotide Transformer: Building and Evaluating Robust Foundation Models for Human Genomics." Nature Methods, 2024.

[11] "Screening of Biosecurity Features in Metagenomic Data with Evo 2 Probes." arXiv:2607.14070. https://arxiv.org/abs/2607.14070

[12] "System requirements for foundation models in IBM watsonx." IBM Documentation. https://www.ibm.com/docs/en/software-hub/5.4.x

[13] "NVIDIA NIM for GenMol Support Matrix." NVIDIA Documentation. https://docs.nvidia.com/nim/bionemo/genmol/latest/support-matrix.html

[14] "Benchmarking genomic foundation models for binary classification of gene fusions." PMC, 2026. https://link.springer.com/content/pdf/10.1186/s13040-026-00553-1.pdf

[15] "Fast and Low-Cost Genomic Foundation Models via Outlier Removal (GERM)." arXiv:2505.00598. https://arxiv.org/pdf/2505.00598.pdf

[16] "How do single-cell foundation model costs compare in 2026." https://quantbio.me/knowledge/how_do_single-cell_foundation_model_costs_compare_in_2026

[17] "DNABERT-2: Efficient Foundation Model and Benchmark For Multi-Species Genomes." ICLR 2024.

[18] "Adversarial Genomic Sequences Could Evade Biosecurity Screening." TAIS 2026. https://tais2026.cc/s/TAIS_final_paper.pdf

[19] "Genomic Language Models: Opportunities and Challenges." PMC. https://pmc.ncbi.nlm.nih.gov/articles/PMC11275703/

[20] "The DNA dialect: a comprehensive guide to pretrained genomic language models." PMC. https://pmc.ncbi.nlm.nih.gov/articles/PMC12953581/

[21] "Large-scale data-driven pre-trained DNA models enhance performance across diverse genomics tasks (SUCCEED)." Nature Communications. https://nature.com/articles/s41467-026-73129-6

[22] "Evo 2: New AI breakthrough can model and design genetic code across all domains of life." Berkeley Engineering, 2025. https://engineering.berkeley.edu/news/2025/02/new-ai-breakthrough-can-model-and-design-genetic-code-across-all-domains-of-life

[23] "OpenGenomeLLM Models Catalog." https://opengenomellm.org/models.html

[24] "A Bioinformatician's Guide to Choosing Genomic Foundation Models." https://www.rewire.it/blog/a-bioinformaticians-guide-to-choosing-genomic-foundation-models/

---

## Summary of Key Findings

- **SOTA**: Evo 2 (40B, 1M context, all domains of life) represents the current frontier; dnaHNet offers superior efficiency via tokenizer-free hierarchical compression.
- **Bottleneck**: Fundamental entropy of genomic sequences limits self-supervised learning effectiveness; tokenization imposes geometric alignment tax.
- **NP-hard**: Quality-aware tokenization bilevel optimization is Σ₂P-hard.
- **Cost**: CAPT reduces inference cost 50% vs full fine-tuning; GERM enables resource-constrained deployment.
- **Scalability**: Subquadratic architectures (StripedHyena, Hyena) enable genome-scale context; scaling laws confirmed on DNA.
- **Biosecurity**: Open-weight GFMs pose dual-use risks; spectral locking and adversarial training provide partial defenses.
- **Failure modes**: Near-uniform distributions, ensemble disagreement, geometric vacuity, and adversarial vulnerability are critical challenges.
