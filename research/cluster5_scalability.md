# Cluster 5: Computational Genomics — Scalability Research

**Date:** 2026-10-04  
**Focus:** Scalability limits, bottlenecks, hardware, cost, biosecurity, failure modes, NP-hard problems

---

## 1. Scalability Overview

Current genomics methods are designed for tens to thousands of samples but must scale to millions to match biomedical data generation rates. The field faces a fundamental gap: sequencing capacity has outstripped computational processing capability, creating a "data deluge" where a typical whole-genome BAM file exceeds 100 GB and joint calling on 150K UK Biobank samples consumed 9.6 million CPU hours with GATK.

**Key insight:** The bottleneck has shifted from data generation (sequencing) to data processing (compute), with computational costs now frequently exceeding sequencing costs.

---

## 2. Bottlenecks

| Bottleneck | Description | Evidence |
|---|---|---|
| **I/O and memory bandwidth** | CPU-to-GPU data transfer limits scaling; not compute capacity | Taylor-Weiner et al. 2019 — "does not scale linearly due to limitations in data transfer" |
| **Joint calling compute** | GATK joint calling on 150K samples: 9.6M CPU hours, 16.6GB RAM/CPU | DPGT bioRxiv 2026 |
| **De Bruijn graph size** | Graph nodes scale with distinct k-mers, not dataset size; wheat genome → 10-17B nodes | IEEE Scalable Assembly 2017 |
| **Graph simplification** | 75% of total assembly time in SWAP2 | IEEE Scalable Assembly 2017 |
| **MSA accuracy degradation** | Alignment quality decreases markedly as sequence count grows | Sievers et al. 2013 |
| **Storage** | BAM files >100GB; population-scale storage prohibitive | Broad Institute; DCS Tools |
| **OOM errors** | Standard tools hit out-of-memory on 10^5–10^6 sample cohorts | DCS Tools bioRxiv 2026 |
| **Egress costs** | Cloud data transfer costs dominate total cost of ownership | Multiple sources |

---

## 3. State-of-the-Art Approaches

### 3.1 GPU Acceleration
- **TensorQTL / SignatureAnalyzer-GPU** (Taylor-Weiner et al. 2019, Genome Biol): >200× runtime reduction, 5–10× cost reduction vs CPU using PyTorch/TensorFlow
- **NVIDIA Parabricks / Embarrassingly_FASTA** (bioRxiv 2026): 26× speedup (15.1h → 35min per 30× WGS), cost drops from ~$120/genome to <$1/genome using spot instances
- **Falcon Computing FPGA**: 50× GATK speedup

### 3.2 Scalable Variant Calling
- **DPGT** (BGI, bioRxiv 2026): Spark-based joint calling; 81% less CPU time than GATK on 2,510 samples; runtime independent of allele counts
- **VC@Scale** (Ahmad et al. 2021): Parallel pre-processing + variant calling
- **GATK4 + GenomicsDB**: Intel-optimized, cloud-deployable, covers all variant classes
- **GLnexus**: gVCF-based joint calling

### 3.3 Scalable Assembly
- **Puzzler** (2025): One-command HiFi+Hi-C assembly; 24 Mbp–6.5 Gbp range; 64 cores/512 GB RAM; checkpoint-based for scale
- **SWAP2** (IEEE 2017): 50B node de Bruijn graph, 16,384 cores, 39 min for 4TB data
- **HipMer**: 15,360 cores scalability on human + wheat
- **hifiasm**: Core assembler for T2T-grade assemblies

### 3.4 Scalable MSA
- **MAFFT G-large-INS-1** (Nakamura et al. 2018): 50,000+ sequences, 5.72GB max memory for 4,000 sequences
- **Convex MSA via dual decomposition** (Zhang et al., PMLR): Entropy-regularized, guaranteed convergence, scales to hundreds of sequences
- **Clustal Omega**: >100,000 sequences but accuracy degrades with scale

### 3.5 CPU-Centric Acceleration
- **DCS Tools** (bioRxiv 2026): 16× speedup over BWA-GATK without specialized hardware; 1.79h per 30× WGS on 32 threads; 80% FASTQ storage reduction, 66% VCF reduction

---

## 4. Hardware Requirements

| Architecture | Use Case | Scalability | Limitations |
|---|---|---|---|
| **Shared-memory multicore** (16 TB RAM) | Large plant genome assembly (wheat) | Up to 128 cores, 4 TB RAM | Single node limit; NUMA overhead |
| **GPU (NVIDIA A10)** | WGS preprocessing, deep learning | 26× speedup; 8 GPUs per node | Data transfer bottleneck; cost at scale |
| **FPGA** | GATK acceleration | 50× speedup | Porting effort; availability; scaling difficulty |
| **Multi-node HPC (MPI)** | Assembly, alignment | 15,000–65,000+ cores | Communication overhead; code porting |
| **Cloud (AWS/GCP/Azure)** | Elastic, population-scale | Near-unlimited | Egress costs; spot instance reliability |
| **Benchtop sequencers** | Decentralized sequencing | 3 Tb/run, $100 genomes | Limited to sequencing, not analysis |

**Key finding:** Specialized hardware (GPU/FPGA) dramatically increases parallelism but faces availability, porting, and heterogeneous scaling challenges. CPU-centric optimization (DCS Tools) offers a hardware-agnostic alternative.

---

## 5. Cost Trade-offs

| Approach | Cost per Genome | Runtime | Trade-off |
|---|---|---|---|
| **CPU on-demand (BWA-GATK)** | ~$17–120 | 15.1 hours | Baseline; cost-prohibitive at scale |
| **GPU on-demand (Parabricks)** | ~$9.50 | 35 min | 18× cheaper than CPU |
| **GPU spot instances** | <$1 | 35 min | Requires transient-intermediate architecture |
| **FPGA (Falcon)** | — | 50× GATK speedup | High porting cost; limited availability |
| **Throughput scaling (600→5K samples/yr)** | 66–82% cost/sample reduction | — | Requires high utilization; maintenance dominates at low volume |
| **Cloud vs on-prem HPC** | Elastic vs CapEx | — | Cloud: no hardware obsolescence; egress costs |

**Key insight:** GPU spot instances with transient intermediates (Embarrassingly_FASTA) flip the conventional wisdom — faster GPU computing is *cheaper* than CPU for embarrassingly parallel genomics workloads.

---

## 6. Biosecurity Governance

- **Five-safes framework** (Shih et al. 2023, iScience): Safe project, safe people, safe data, safe settings, safe outputs — implemented in RAPTOR serverless cloud-native genomics platform
- **Cloud security challenges**: S3 endpoint exposure, data sovereignty, multi-tenant isolation
- **Genomic data sensitivity**: Population-scale data requires governance for re-identification risk, data sharing agreements, and cross-border transfer
- **Biosecurity implications of scalability**: Lower costs and decentralized sequencing lower barriers for both beneficial and potentially harmful applications; governance frameworks must scale with computational accessibility

---

## 7. Failure Modes

| Failure Mode | Root Cause | Mitigation |
|---|---|---|
| **Out-of-memory (OOM)** | Cohort sizes 10^5–10^6 exceed RAM | Low-memory index modes; distributed computing |
| **I/O bottleneck** | CPU-GPU data transfer saturation | Batch processing; transient intermediates |
| **Sub-linear scaling** | Communication overhead in MPI; data transfer | Algorithm redesign; hybrid methods |
| **Accuracy degradation (MSA)** | Error accumulation with sequence count | Iterative refinement; structural priors |
| **De Bruijn graph explosion** | Distinct k-mer count, not data size | Graph simplification; sparse representations |
| **Spot instance preemption** | Cloud capacity fluctuations | Checkpoint-based workflows (Puzzler) |
| **Hardware obsolescence** | 3–5 year refresh cycles | Cloud migration; containerized pipelines |
| **Egress cost explosion** | Cloud data transfer pricing | Process-at-source; transient intermediates |

---

## 8. NP-Hard Problems in Computational Genomics

| Problem | Complexity | Source |
|---|---|---|
| **De Bruijn graph assembly** (Euler path) | NP-hard | IEEE Scalable Assembly 2017 |
| **Genome rearrangement with duplicates** (breakpoints, common intervals, conserved intervals) | APX-hard | JGAA — Bulteau et al. |
| **Exemplar breakpoint distance** | NP-complete | JGAA — Bulteau et al. |
| **Multiple Sequence Alignment** (sum-of-pairs) | NP-hard | Classical result |
| **Shortest common superstring** | NP-hard | Classical result |

**Implication:** Exact solutions are infeasible for large instances; all practical tools use heuristics, approximations, or restricted problem formulations.

---

## 9. Open Source Projects

| Project | Domain | Scalability Feature |
|---|---|---|
| **GATK4** (Broad) | Variant calling | Cloud-deployable, ML-based, all variant classes |
| **Hail** (Broad) | Genetic data analysis | Distributed computing, exploratory at scale |
| **GenomeTools** | Genome analysis | Memory-efficient k-mer counting, compressed sequences |
| **DPGT** (BGI) | Joint variant calling | Spark-based, million-scale cohorts |
| **Puzzler** | Genome assembly | Checkpoint-based, one-command, 24 Mbp–6.5 Gbp |
| **MAFFT** | MSA | MPI parallel, 50K+ sequences |
| **hifiasm** | Assembly | HiFi read assembly, T2T quality |
| **NVIDIA Parabricks** | GPU-accelerated genomics | 26× speedup, cloud-native |
| **DCS Tools** | WGS pipeline | CPU-optimized, 16× speedup, hardware-agnostic |
| **GLnexus** | Joint calling | gVCF-based, scalable |
| **VC@Scale** | Variant calling | Parallel pre-processing + calling |
| **RAPTOR** | Genomics repository | Serverless, five-safes security |

---

## 10. Most Cited Papers

1. **Taylor-Weiner et al. 2019** — "Scaling computational genomics to millions of individuals with GPUs" — *Genome Biology* — DOI: 10.1186/s13059-019-1836-7 — PMID: 31675989
2. **Sievers et al. 2013** — "Making automated multiple alignments of very large numbers of protein sequences" — *Bioinformatics* 29(8):989–995 — DOI: 10.1093/bioinformatics/btt093
3. **Nakamura et al. 2018** — "Parallelization of MAFFT for large-scale multiple sequence alignments" — *Bioinformatics* 34(14):2490–2492 — DOI: 10.1093/bioinformatics/bty121
4. **Ahmad et al. 2021** — "VC@Scale: Scalable and high-performance variant calling" — PMC8424057
5. **Shih et al. 2023** — "A five-safes approach to a secure and scalable genomics data repository" — *iScience* — Cited by 10
6. **Zhang et al. 2017** — "Scalable Convex Multiple Sequence Alignment via Entropy-Regularized Dual Decomposition" — *PMLR* v54
7. **Bulteau et al.** — "On the Approximability of Comparing Genomes with Duplicates" — *JGAA*
8. **DPGT** (2026) — "A spark based high-performance joint variant calling tool" — bioRxiv
9. **Embarrassingly_FASTA** (2026) — "Enabling Recomputable, Population-Scale Pangenomics" — bioRxiv
10. **Puzzler** (2025) — "scalable one-command platinum-quality genome assembly" — *Bioinformatics Advances*

---

## 11. Scalability Limits Summary

1. **Theoretical:** NP-hardness of core problems (assembly, MSA, genome rearrangement) means exact solutions are impossible; all practical tools are heuristic
2. **Algorithmic:** Sub-linear scaling due to communication overhead, I/O bottlenecks, and data transfer limits
3. **Hardware:** Single-node memory limits; heterogeneous scaling difficulty; hardware obsolescence
4. **Economic:** Egress costs, spot instance reliability, maintenance costs at low throughput
5. **Accuracy:** MSA quality degrades with scale; graph simplification introduces errors
6. **Governance:** Biosecurity frameworks must scale with computational accessibility; five-safes approach provides a model

---

## References

- Taylor-Weiner A, et al. Scaling computational genomics to millions of individuals with GPUs. *Genome Biol*. 2019;20(1):228. DOI: 10.1186/s13059-019-1836-7
- Ahmad T, et al. VC@Scale: Scalable and high-performance variant calling. 2021. PMC8424057
- DPGT: A spark based high-performance joint variant calling tool. *bioRxiv*. 2026. DOI: 10.64898/2026.03.02.709184
- Puzzler: scalable one-command platinum-quality genome assembly from HiFi and Hi-C. *Bioinformatics Advances*. 2025. PMC12820402
- Scalable Assembly for Massive Genomic Graphs. *IEEE*. 2017. DOI: 10.1109/...7973755
- Nakamura T, et al. Parallelization of MAFFT. *Bioinformatics*. 2018;34(14):2490–2492. DOI: 10.1093/bioinformatics/bty121
- Sievers F, et al. Making automated multiple alignments of very large numbers of protein sequences. *Bioinformatics*. 2013;29(8):989–995. DOI: 10.1093/bioinformatics/btt093
- Computational Strategies for Scalable Genomics Analysis. *PMC*. 2021. PMC6947637
- DCS Tools: A high-performance, resource-efficient and scalable computing suite. *bioRxiv*. 2026. DOI: 10.64898/2026.03.13.711253
- Cloud computing in population-scale genomics. *J Genet Genomics*. 2025. DOI: 10.5734/jgm.2025.22.2.37
- Genomics costing tool. *Frontiers in Public Health*. 2024. DOI: 10.3389/fpubh.2024.1498094
- Shih CC, et al. A five-safes approach to a secure and scalable genomics data repository. *iScience*. 2023. DOI: 10.1016/j.isci.2023.106605
- Embarrassingly_FASTA. *bioRxiv*. 2026. DOI: 10.64898/2026.02.02.703356
- On the Approximability of Comparing Genomes with Duplicates. *JGAA*. 
- Zhang J, et al. Scalable Convex Multiple Sequence Alignment via Entropy-Regularized Dual Decomposition. *PMLR*. 2017;v54
- Broad Institute. GATK4 release. 2018.
- Broad Institute. Harnessing the flood: Scaling up data science in the big genomics era.
- Scalable Genomics (company). Tracxn profile.
