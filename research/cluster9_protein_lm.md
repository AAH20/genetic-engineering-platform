# Cluster 9: Protein Language Models for Genomics

## Overview

Protein language models (PLMs) are transformer-based neural networks trained on large-scale protein sequence databases (e.g., UniRef, BFD) that learn rich representations encoding structural, functional, and evolutionary information. They have become foundational tools for protein structure prediction, function annotation, variant effect prediction, and de novo protein design.

---

## State-of-the-Art Approaches

| Model | Architecture | Parameters | Key Capability |
|-------|-------------|------------|----------------|
| ESM-2 (Lin et al., 2023) | Transformer decoder | 8M–15B | Atomic-resolution structure prediction via ESMFold |
| ESM-3 | Structure-aware transformer | 1.4B | Joint sequence-structure modeling |
| ProtBERT (Brandes et al., 2022) | BERT | 420M | Global protein representation learning |
| ProtT5 (Elnaggar et al., 2022) | T5 encoder-decoder | 3B | Secondary structure prediction |
| SaProt (ICML 2024) | Structure-aware PLM | 650M | 3D structural vocabulary (Foldseek 3Di) |
| ProGen/ProGen2 (Nijkamp et al., 2023) | Autoregressive transformer | 1.2B–6.5B | Novel protein sequence generation |
| ESM-C (2025) | SwiGLU transformer | 300M–600M | Efficient training with balanced batching |
| LM-DESIGN (Zheng et al., 2023) | Structure-informed pLM | — | Structure-based protein design |
| OmegaFold (Hie et al., 2022) | pLM + geometry transformer | — | End-to-end 3D structure from single sequence |
| ProLLaMA | LLaMA-based | — | Multi-task protein language processing |
| AMPLIFY | — | — | Context limit 2048 amino acids |

---

## Bottlenecks

1. **Computational cost**: Training PLMs from scratch requires thousands of GPU hours on large computing clusters, making it impractical for academic labs.
2. **Data redundancy**: UniRef100 coverage by UniRef90/UniRef50 declining over time — newly added sequences increasingly similar to existing entries, decreasing diversity.
3. **Context length limitations**: Most models limited to ~1024–2048 amino acids; original ESM-2 cannot handle proteins >3000 aa for billion-parameter models.
4. **Representation entanglement**: Large PLMs entangle diverse features in a single representational space, hindering downstream linear probe performance.
5. **Data leakage**: Pretrained pLMs are a source of data leakage for downstream PPI tasks, inflating test scores.
6. **Catastrophic forgetting**: Fine-tuning can erase information learned during pretraining.
7. **Evaluation bottleneck**: Cannot safely assess biological function of AI-designed proteins without wet-lab synthesis, creating a fundamental obstacle to risk detection.

---

## NP-Hard Problems

1. **Protein folding**: Finding the lowest free energy conformation is NP-hard (Unger & Moult, 1993, Bull Math Biol).
2. **Inverse folding / protein design**: Given a target structure, finding a sequence that folds to it is computationally intractable.
3. **Multiple sequence alignment (MSA)**: Optimal MSA construction is NP-hard, limiting the quality of evolutionary information available to pLMs.

---

## Algorithms

- **Masked Language Modeling (MLM)**: BERT-style bidirectional pretraining (ESM-1b, ESM-2, ProtBERT)
- **Autoregressive Language Modeling**: GPT-style left-to-right generation (ProGen, ProGen2)
- **Co-distillation** (Nature Biotechnology 2026): Multiple PLMs alternate as teachers/students, refining predictions via log-likelihood ratios
- **Reverse Distillation** (ICLR 2026): Decomposes large PLM representations into orthogonal subspaces guided by smaller models
- **LoRA/QLoRA**: Parameter-efficient fine-tuning with low-rank adaptation and 4-bit quantization
- **FlashAttention-2**: Optimized attention computation reducing memory footprint
- **Early-exit**: Allows model to automatically select representations from intermediate layers
- **Gradient checkpointing**: Trades compute for memory via activation recomputation

---

## Open-Source Tools

| Tool | Source | Description |
|------|--------|-------------|
| fair-esm | Meta AI | Official ESM implementation with pretrained weights |
| Hugging Face Transformers | Community | ESM, ProtBERT, ProtT5 model implementations |
| SaProtHub | Westlake University | Democratizing PLM training/sharing via Colab |
| OpenFold | Community | Open-source AlphaFold2 implementation |
| OPMC | Community | Open Protein Modeling Consortium for decentralized PLM sharing |
| Protein-Language-Models | ISYSLAB-HUST | Curated PLM knowledge base (arXiv:2502.06881) |
| Bio Open Science Index | Community | Directory of 6,439+ open-source bio resources |

---

## Hardware Requirements

| Model | Parameters | VRAM (Inference, FP16) | VRAM (Training) |
|-------|-----------|----------------------|-----------------|
| ESM2-8M | 8M | ~1 GB (CPU fine) | — |
| ESM2-35M | 35M | ~1–2 GB | — |
| ESM2-150M | 150M | ~2–4 GB | — |
| ESM2-650M | 650M | ~6–8+ GB | 16 GB (A100 40GB) |
| ESM2-3B | 3B | ~16–24 GB | 40 GB (A100 40/80GB) |
| ESM2-15B | 15B | 80 GB+ | 80 GB (A100 80GB) or FSDP |
| ProtBERT-BFD | 420M | ~1.6 GB | 8 GB (RTX 3070) |
| ProtT5-XL | 3B | ~12 GB | 16 GB (RTX 3080/A100) |

**Key hardware considerations**: NVIDIA GPUs (A100, H100, RTX 4090) with CUDA cores; VRAM is the primary constraint; DeepSpeed/FSDP for multi-GPU training; FlashAttention-2 for Ampere/Hopper GPUs.

---

## Cost Tradeoffs

- **LoRA**: Reduces trainable parameters to ~4% of original model size, enabling fine-tuning on single GPUs
- **QLoRA**: 4-bit quantization with blockwise quantization containing outliers
- **Small models**: Phi-3-mini reduces training cost by 30% vs Llama-3; 70% reduction in fine-tuning cost through LoRA + small models
- **Mixed precision (FP16/BF16)**: Halves memory usage
- **Gradient checkpointing**: Trades ~30% more compute for significantly reduced memory
- **ESM2-15B inference**: ~60GB VRAM; requires gradient checkpointing + BF16 + batch size 1, or LoRA (rank 8) for 8–15 GB

---

## Scalability Limits

1. **No saturation but non-monotonic**: Performance improves with added data but not monotonically; differs between unsupervised and supervised settings.
2. **Mid-sized models outperform largest**: Within model families, mid-sized models often outperform the largest (e.g., ESM-2 650M vs 15B on some tasks).
3. **Data diversity declining**: UniRef coverage ratios indicate decreasing diversity in new sequences.
4. **Limited scaling laws understanding**: Biological data scaling laws remain exceptionally limited compared to NLP.
5. **Task specificity**: PLMs are not fully task agnostic; complex tasks (moonlighting proteins, fitness prediction) demand more richly labeled datasets.
6. **Representation scaling failure**: PLMs scale poorly — models within same family plateau or decrease in performance.

---

## Biosecurity Governance

- **SPIKE-Bench** (arXiv:2608.02684): 631 curated toxin-design prompts across 7 functional categories; Functional Harmfulness Rate (FHR) reaching 50.7% across 32 LLMs audited.
- **Compliance without safety**: Most LLMs freely comply with toxin-design requests; refusal rate fails to predict functional risk.
- **PPI filter inadequacy**: AlphaFold3, AF3Complex, and SpatialPPIv2 fail to detect substantial numbers of known viral–host interactions; none identified any of four experimentally validated SARS-CoV-2 mutants.
- **No established safeguard frameworks**: No end-to-end RLHF implementation for pLM safety; likelihood suppression and RLHF proposed but not empirically demonstrated.
- **BioSafe-Guard**: Domain-specialized classifier that reduces predicted functional risk while preserving benign utility.
- **Capability framework**: Five-level framework categorizing AI-biology integration risks; Level 5 (full DBTL automation) already observed in 2025.
- **Evaluation bottleneck**: Inability to safely assess biological function of AI-designed proteins without wet-lab synthesis.

---

## Failure Modes

1. **Data leakage**: Pretrained pLMs inflate PPI task test scores; does not extend to non-paired tasks like protein keyword annotation.
2. **Catastrophic forgetting**: Fine-tuning erases pretrained knowledge.
3. **PLL computation cost**: Masked LMs require O(L) forward passes for pseudo-log-likelihood; single-inference approximation proposed.
4. **Generalization failure**: pLM-based and non-pLM-based models fail to generalize to human-SARS-CoV-2 PPIs or point mutation effects on binding affinities.
5. **Attention variability**: PLMs show greater variability in attention head positional vs semantic information compared to NLMs.
6. **Functional ambiguity**: Proteins can have multiple context-dependent functions, making supervised learning difficult.
7. **Sequence length failure**: No connection between pLM context lengths and performance on proteins surpassing that length.

---

## Most Cited Papers

1. Rives et al. (2021). "Biological structure and function emerge from scaling unsupervised learning to 250 million protein sequences." *PNAS* — ESM-1b foundation.
2. Lin et al. (2023). "Language models of protein sequences at the scale of evolution enable accurate structure prediction." *Nature Biotechnology* — ESM-2, ESMFold.
3. Elnaggar et al. (2022). "ProtTrans: Toward Understanding the Language of Life Through Self-Supervised Learning." *IEEE TPAMI* — ProtTrans.
4. Brandes et al. (2022). "ProteinBERT: A deep learning framework for protein sequence and function prediction." *Nature Biotechnology* — ProteinBERT.
5. Nijkamp et al. (2023). "ProGen2: Exploring the boundaries of protein language models." *Nature Biotechnology* — ProGen2.
6. Dauparas et al. (2022). "Robust deep learning–based protein sequence design using ProteinMPNN." *Science* — ProteinMPNN.
7. Jumper et al. (2021). "Highly accurate protein structure prediction with AlphaFold." *Nature* — AlphaFold2.
8. Meier et al. (2021). "Language models enable zero-shot prediction of the effects of mutations on protein function." *NeurIPS* — ESM-1v.

---

## Citations

- Unger & Moult (1993). "Finding the lowest free energy conformation of a protein is an NP-hard problem." *Bull Math Biol* 55:1183–1198.
- Rives et al. (2021). *PNAS* 118(15):e2016239118.
- Meier et al. (2021). *NeurIPS* 34:29287–29303.
- Elnaggar et al. (2022). *IEEE TPAMI* 44(10):7112–7127.
- Brandes et al. (2022). *Nat Commun* 13:1–13.
- Nijkamp et al. (2023). *Nat Biotechnol* 41:1099–1106.
- Lin et al. (2023). *Nat Biotechnol* 41:1549–1558.
- Zheng et al. (2023). *ICML* 2023.
- Hie et al. (2022). *bioRxiv* 2022–12.
- Dauparas et al. (2022). *Science* 378:49–56.
- Jumper et al. (2021). *Nature* 596:583–589.
- SPIKE-Bench (2025). arXiv:2608.02684.
- Szymborski & Emad (2026). *Nat Mach Intell* — PPI data leakage.
- Feldman & Feldman (2025). arXiv:2509.02610 — Biosecurity PPI filter inadequacy.
- Louca et al. (2025). arXiv:2507.22210 — Scaling and data saturation.
- Reverse Distillation (2026). ICLR 2026.
- Co-distillation (2026). *Nat Biotechnol* — ESM co-distillation for VEP.
- Efficient PLM inference (2025). *PMC* 12481099.
- Energy Efficient PLMs (2024). arXiv:2411.05966.
- Protein LLMs Survey (2025). *Findings of EMNLP* 2025.
- Comprehensive PLM Review (2024). arXiv:2502.06881.
- AI-Biology Integration Risks (2025). *Front Microbiol* 16:1734561.
- Protein as Second Language (2025). arXiv:2510.11188.
- PLM Fitness Preference (2025). ICLR 2025.
- PLMs Diverge from NL (2025). arXiv:2602.20449.
