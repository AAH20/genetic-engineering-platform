# Cluster 5: Variant Calling — Computational Genomics Research

**Date:** 2026-10-04
**Focus:** Variant calling tools, algorithms, hardware, cost, scalability, and biosecurity

---

## 1. State-of-the-Art Approaches

Variant calling is the computational process of identifying genetic variants (SNPs, indels, MNPs, structural variants) from aligned sequencing reads relative to a reference genome. The field has undergone a paradigm shift from hand-crafted statistical models to deep learning-based approaches.

### 1.1 Traditional Statistical Callers

- **GATK HaplotypeCaller** (Broad Institute): Uses local de novo assembly of reads in active regions, realignment against candidate haplotypes, and PairHMM for genotype likelihoods. The GVCF-based workflow enables scalable multi-sample joint genotyping without reprocessing all samples. VQSR (Variant Quality Score Recalibration) applies a Gaussian mixture model for filtering. GATK is the most widely cited variant caller and the clinical gold standard. [1, 2]

- **FreeBayes**: Bayesian haplotype-based caller that evaluates literal read sequences rather than alignment coordinates, avoiding alignment ambiguity. Excels at complex variants (MNPs, composite events) and non-model organisms. A 30× WGS sample calls in ~4–6 hours on a 16-core machine with 32 GB RAM. [3, 4]

- **BCFtools** (samtools ecosystem): Provides `bcftools mpileup` + `bcftools call` for consensus-based variant calling. Over 60 subcommands for VCF/BCF manipulation (filter, merge, annotate, query, norm). Processes a 30× WGS BAM in under 90 minutes—3–4× faster than FreeBayes and 6–8× faster than GATK. The multiallelic calling model (`-m`) is recommended. [5, 6]

### 1.2 Deep Learning Callers

- **DeepVariant** (Google Health): CNN-based caller that encodes read pileups as image tensors and classifies genotypes using Inception-v2/v3 architecture. Achieves SNP F1 scores of 99.9% on Illumina and PacBio HiFi data. Supports germline calling across Illumina, PacBio HiFi, ONT R10.4.1, and hybrid data. Automated filtering eliminates post-calling refinement. However, computational cost is high: ~5 hours on 96 vCPUs (m5.24xlarge) or ~8 minutes on NVIDIA DGX GPU for 30× WGS. [7, 8, 9]

- **DeepTrio**: Extension of DeepVariant for trio-based analysis, leveraging Mendelian inheritance to improve de novo mutation detection. Requires even greater computational resources. [7, 10]

- **Clair3**: DL-based caller with a compact architecture (~2M parameters vs DeepVariant's ~20M). Achieves SNP F1 of 99.32% on ONT and 99.70% on PacBio HiFi at 30× coverage. GPU-accelerated version completes 30× WGS in 12–20 minutes on a single NVIDIA 4090. [11, 12]

- **DNAscope** (Sentieon): ML-assisted caller that integrates ML into GATK HaplotypeCaller pipeline. Not fully DL-based; optimized for speed and low memory. Commercial. [7, 13]

### 1.3 Benchmark Performance

A comparative study on NA12878 (Genome in a Bottle) benchmarked seven callers: DeepVariant achieved highest precision (0.7869) and F1-score (0.8754) on chromosome 20. Strelka2 excelled in precision (0.8326) for whole-genome, while Octopus demonstrated superior recall (0.9838). FreeBayes showed high sensitivity but lower precision. [14]

---

## 2. Bottlenecks

1. **Computational cost of DL callers**: DeepVariant requires ~5 hours on 96 vCPUs or ~8 minutes on GPU for a single 30× WGS sample. This creates barriers for large-cohort studies and time-sensitive clinical applications without HPC/cloud access. [7, 8]

2. **Accuracy in difficult genomic regions**: Repetitive regions, GC-rich areas, and low-complexity sequences remain challenging for all callers. ONT data shows significantly lower InDel accuracy (76.8% F1 for DeepVariant) due to higher base-calling error rates. [7, 15]

3. **Joint genotyping scalability**: Traditional joint calling is computationally expensive and less scalable than single-sample calling. Harmonizing overlapping alleles is algorithmically intricate, and the number of overlapping alleles increases with cohort size. [16]

4. **I/O bottlenecks**: Running from NFS or object storage adds 20–40% to runtime due to I/O wait. NVMe staging is essential for GPU-accelerated pipelines. [17]

5. **Model transparency and overfitting**: DL-based callers act as black boxes. Models trained on human data may not generalize to other organisms without retraining. Overfitting to training benchmarks is a concern. [18]

6. **Structural variant detection**: Most DL callers focus on small variants (SNPs, indels). SV detection remains a separate, challenging problem requiring different approaches (de novo assembly or long-read alignment). [15]

7. **Serverless computational ceilings**: Serverless workflows for joint variant calling are limited by the computational ceilings of FaaS platforms, setting an upper limit to workflow scaling. [19]

---

## 3. Hardware Requirements

### 3.1 CPU-Only Pipelines

| Tool | 30× WGS Runtime | Cores | RAM |
|------|----------------|-------|-----|
| GATK HaplotypeCaller | 8–14 hours | 8–16 | 32–64 GB |
| FreeBayes | 4–6 hours | 16 | 32 GB |
| BCFtools mpileup+call | <90 minutes | 8–16 | 16–32 GB |
| DeepVariant (CPU) | ~5 hours | 96 (m5.24xlarge) | 192 GB |

[4, 6, 8, 20]

### 3.2 GPU-Accelerated Pipelines

| Hardware | Concurrent 30× WGS Samples | VRAM per Sample | CPU Threads |
|----------|---------------------------|-----------------|-------------|
| NVIDIA T4 | 1–2 | ~35–40 GB | 24–32 |
| H100 SXM5 (80GB) | 1–2 | ~35–40 GB | 16–32 |
| H200 SXM5 (141GB) | 3 | ~35–40 GB | 32–48 |
| B200 SXM6 (192GB) | 4 | ~35–40 GB | 48–64 |
| NVIDIA RTX 4090 | 1 | ~24 GB | 32 |

[11, 12, 17, 21]

### 3.3 Storage Requirements

A single 30× WGS sample generates:
- 50–80 GB compressed FASTQ input
- 120–150 GB intermediate BAM
- 2–4 GB final VCF

NVMe staging is strongly recommended. NFS/object storage mounts add 20–40% runtime overhead. [17]

### 3.4 GPU-Accelerated Runtimes (Parabricks)

| Pipeline Stage | CPU Baseline | GPU (H100) |
|----------------|-------------|------------|
| BWA-MEM alignment | 8–12 hr | 8–12 min |
| MarkDuplicates | 1–2 hr | 5–10 min |
| BQSR | 2–4 hr | 10–15 min |
| HaplotypeCaller | 8–14 hr | 8–15 min |
| DeepVariant | 4–6 hr | 3–5 min |

[17]

---

## 4. Cost Tradeoffs

### 4.1 Cloud Computing Costs

- **Cloud-native WGS pipeline**: ~$16.5 per sample for 55× WGS (alignment + variant calling), ~18.4 minutes. [22]
- **500 WGS samples (30×)**: ~$22.83/sample compute + ~$14,472 storage = ~$40,450 Year 1 total (including 2× contingency). [23]
- **Serverless joint calling**: $2–$70 for 2–62 samples (GATK best practices on AWS/Azure). [19]
- **GenomeKey/COSMOS**: ~$50 per genome for up to 25 genomes. [24]

### 4.2 Instance Pricing (Representative)

| Instance | Specs | Hourly Rate | Use Case |
|----------|-------|-------------|----------|
| cpu2mem8a | 2 CPU, 8GB | $0.09 | Preprocessing |
| cpu4mem32a | 4 CPU, 32GB | $0.23 | BWA, variant calling |
| cpu8mem64a | 8 CPU, 64GB | $0.45 | GATK, multi-sample |
| cpu16mem128a | 16 CPU, 128GB | $0.90 | Assembly |
| gpu1mem64 | 1 A10G, 64GB | $1.62 | DL inference |
| gpu4mem96 | 4 A10G, 96GB | $5.67 | Large model training |

[23]

### 4.3 Cost Optimization Strategies

- **Spot/preemptible instances**: 70–90% discount vs on-demand; ideal for fault-tolerant batch processing. [22]
- **Storage tiering**: S3 Standard ($18/TB/mo) → Intelligent-Tiering ($11–18/TB/mo) → Glacier ($3.50/TB/mo). [23]
- **GPU acceleration**: 60× speedup for HaplotypeCaller, 30× for DeepVariant — reduces cost per sample despite higher hourly rate. [21]
- **Reserved instances**: Significant discounts for long-term commitments. [22]

---

## 5. Scalability Limits

### 5.1 Population-Scale Achievements

- **All of Us / Celeste**: Processed up to 9,000 WGS samples monthly using serverless + container orchestration. [25]
- **UK Biobank WES**: 500,000 individuals processed with DeepVariant. [7]
- **1KGP cohort calling**: DeepVariant + GLnexus framework for scalable joint genotyping of large cohorts. [16]

### 5.2 Scalability Strategies

1. **GVCF-based joint genotyping**: Single-sample calling to gVCF, then joint genotyping. Avoids reprocessing all samples when adding new ones. [1, 16]
2. **GLnexus**: Scalable merging tool adapted for DeepVariant gVCFs; handles allele normalization and cohort-scale genotyping. [16]
3. **Chromosome batching**: Strategically batching by chromosome improves runtime and cost. [24]
4. **Serverless orchestration**: SWEEP WMS on AWS/Azure for automatic scaling, but limited by FaaS computational ceilings. [19]
5. **Hardware-accelerated implementations**: DRAGEN, Parabricks for FPGA/GPU acceleration. [25]

### 5.3 Scaling Bottlenecks

- Joint genotyping of large cohorts: overlapping allele harmonization is algorithmically intricate; error aggregation across many samples. [16]
- Serverless platforms: computational ceilings limit maximum problem size. [19]
- On-premise HPC: fixed storage, high maintenance costs, hardware obsolescence in 3–5 years. [22]
- Data transfer: Moving terabyte-scale datasets to cloud is a bottleneck. [22]

---

## 6. Failure Modes

1. **False positives in repetitive/low-complexity regions**: All callers struggle with homopolymers, STRs, and segmental duplications. [15, 18]
2. **Reference bias**: Alignment-based callers systematically miss variants in regions divergent from the reference. FreeBayes mitigates this by using literal read sequences. [3]
3. **Sequencing error propagation**: ONT's higher base-calling error rates significantly reduce InDel accuracy (DeepVariant InDel F1 drops to 76.8% on ONT). [7]
4. **Batch effects**: Multi-sample calling can introduce systematic artifacts that violate Hardy-Weinberg equilibrium. [16]
5. **Model overfitting**: DL callers may overfit to training benchmarks (e.g., GIAB) and perform poorly on novel data or non-human organisms. [18]
6. **Contamination/sample swaps**: BCFtools gtcheck can detect these, but they remain a failure mode in large cohorts. [6]
7. **VQSR failure at low coverage**: GATK's VQSR requires sufficient variant density; fails on small cohorts or gene panels. [1]
8. **DeepVariant ploidy limitation**: Only supports diploid organisms (hom-alt, het, hom-ref genotypes). [9]

---

## 7. NP-Hard Problems

1. **Haplotype assembly**: Reconstructing haplotypes from short reads is NP-hard in general. GATK's local de novo assembly and FreeBayes' haplotype-based calling are heuristic approximations. [1, 3]

2. **Multiple sequence alignment (MSA)**: Fundamental to variant calling; exact MSA is NP-hard. All aligners (BWA-MEM, minimap2) use heuristics. [15]

3. **Joint genotyping / allele harmonization**: Merging overlapping alleles across large cohorts is algorithmically intricate; the number of overlapping alleles increases with cohort size. [16]

4. **Structural variant detection**: De novo assembly-based SV detection involves genome assembly, which is NP-hard. Read alignment-based SV detection involves discordant read pair and split read analysis, also computationally hard. [15]

5. **Variant phasing**: Determining the haplotype phase of variants is NP-hard in general. Long-read technologies and population-based phasing (e.g., LongPhase) provide approximations. [12]

---

## 8. Most Cited Papers

1. **McKenna et al. (2010)** — "The Genome Analysis Toolkit: a MapReduce framework for analyzing next-generation DNA sequencing data." *Genome Research*. GATK original paper. [1]
2. **Poplin et al. (2018)** — "Creating a universal SNP and small indel variant caller with deep neural networks." *Nature Biotechnology*. DeepVariant original paper. [8]
3. **Garrison & Marth (2012)** — "Haplotype-based variant detection from short-read sequencing." arXiv. FreeBayes original paper. [3]
4. **Danecek et al. (2021)** — "Twelve years of SAMtools and BCFtools." *GigaScience*. BCFtools review. [5]
5. **Van der Auwera et al. (2013)** — "From FastQ data to high confidence variant calls: the Genome Analysis Toolkit best practices pipeline." *Current Protocols in Bioinformatics*. GATK Best Practices. [1]
6. **Kolesnikov et al. (2021)** — "DeepTrio: variant calling in trios with deep learning." *Nature Biotechnology*. [10]
7. **Zheng et al. (2022)** — "Clair3: accurate long-read variant calling with pileup, full-alignment, and deep learning." *Nature Biotechnology*. [12]
8. **Lin et al. (2018)** — "Scalable and accurate joint variant calling with GLnexus." *Nature Biotechnology*. [16]

---

## 9. Open Source Projects

| Project | Language | License | Description |
|---------|----------|---------|-------------|
| [GATK4](https://github.com/broadinstitute/gatk) | Java | BSD-3 | Broad Institute's variant calling and genotyping suite |
| [DeepVariant](https://github.com/google/deepvariant) | Python/C++ | Apache-2.0 | Google's CNN-based variant caller |
| [DeepTrio](https://github.com/google/deepvariant) | Python/C++ | Apache-2.0 | Trio variant caller built on DeepVariant |
| [BCFtools](https://github.com/samtools/bcftools) | C | MIT/BSD | VCF/BCF manipulation and variant calling |
| [FreeBayes](https://github.com/freebayes/freebayes) | C++ | MIT | Bayesian haplotype-based variant caller |
| [Clair3](https://github.com/HKU-BAL/Clair3) | Python/C++ | BSD-3 | Long-read variant caller with GPU acceleration |
| [GLnexus](https://github.com/dnanexus-rnd/GLnexus) | C++ | MIT | Scalable joint genotyping/merging |
| [SAMtools](https://github.com/samtools/samtools) | C | MIT | BAM/CRAM manipulation |
| [DeepSomatic](https://github.com/google/deepvariant) | Python/C++ | Apache-2.0 | Somatic variant calling with DL |
| [Nucleus](https://github.com/google/nucleus) | Python/C++ | Apache-2.0 | Genomics file I/O library for TensorFlow |
| [Octopus](https://github.com/luntergroup/octopus) | C++ | MIT | Haplotype-based variant caller with random forest filtering |
| [Strelka2](https://github.com/Illumina/strelka) | C++ | GPL-3.0 | Somatic and germline variant caller |
| [VarScan2](https://github.com/dkoboldt/varscan) | Java | MIT | Pileup-based somatic/germline caller |
| [LoFreq](https://github.com/CSB5/lofreq) | Python | MIT | Low-frequency variant caller |
| [Parabricks](https://docs.nvidia.com/clara/parabricks/) | CUDA | Commercial | GPU-accelerated genomics pipelines |

---

## 10. Biosecurity Governance

### 10.1 Dual-Use Research of Concern (DURC)

Variant calling itself is not typically classified as DURC, but the broader context of genomic technologies raises biosecurity considerations:

- **NSABB Framework**: The National Science Advisory Board for Biosecurity provides oversight for dual-use life sciences research. DURC is defined as research that, based on current understanding, can be reasonably anticipated to provide knowledge, information, products, or technologies that could be directly misapplied to pose a threat to public health, agriculture, or national security. [26, 27]

- **Gain-of-function research**: The 2011 H5N1 controversy established that enhancing transmissibility of pathogens triggers DURC review. Variant calling could theoretically be applied to engineer pathogen genomes. [27]

### 10.2 Relevant Governance Frameworks

- **NSABB Proposed Oversight Framework** (2023): Institutional review of dual-use research, PI-led initial evaluation, responsible communication of sensitive findings. [26]
- **Biological Weapons Convention (BWC)**: International treaty prohibiting biological weapons; relevant to genomic engineering of pathogens. [28]
- **FAIR/SAFE principles**: Findable, Accessible, Interoperable, Reusable data principles with Secure and Authorized FAIR Environment for genomic data sharing. [22]
- **Institutional Biosafety Committees (IBCs)**: Local oversight for recombinant DNA research. [26]

### 10.3 Variant Calling-Specific Concerns

- **Pathogen genome analysis**: Variant calling on pathogen sequences could identify virulence factors or drug resistance markers with dual-use potential.
- **Synthetic biology integration**: Combined with DNA synthesis, variant calling data could guide engineering of enhanced pathogens.
- **DIY biohacking**: Increasingly accessible cloud-based variant calling lowers barriers for non-experts. [28]
- **Data security**: Large-scale genomic databases (e.g., All of Us, UK Biobank) require robust access controls to prevent misuse. [25]

---

## 11. Summary and Recommendations

### Tool Selection Guide

| Use Case | Recommended Tool | Rationale |
|----------|-----------------|-----------|
| Clinical germline (human) | GATK HaplotypeCaller + VQSR | Regulatory-grade, best practices validated |
| Research germline (high accuracy) | DeepVariant | Highest F1, automated filtering |
| Non-model organisms | FreeBayes | Fewer assumptions, handles complex variants |
| Rapid QC / preliminary | BCFtools mpileup+call | Fastest, lightweight |
| Long-read (ONT/PacBio) | Clair3 | Optimized for long reads, GPU-accelerated |
| Trio/family studies | DeepTrio | Leverages Mendelian inheritance |
| Somatic (tumor-normal) | Mutect2 / Strelka2 / DeepSomatic | Somatic-specific models |
| Large cohorts (1000+) | DeepVariant + GLnexus | Scalable joint genotyping |
| Resource-limited | FreeBayes or BCFtools | Lower compute requirements |

### Key Trends

1. **Deep learning dominance**: DL callers (DeepVariant, Clair3) consistently outperform traditional methods in accuracy benchmarks.
2. **GPU acceleration**: Essential for practical DL-based calling; 10–60× speedups over CPU.
3. **Cloud-native pipelines**: Serverless and container orchestration enable population-scale processing.
4. **Pangenome integration**: Moving beyond single reference to pangenome-aware calling (vg-mapped DeepVariant).
5. **Long-read transition**: ONT and PacBio HiFi increasingly preferred for SV detection and phasing.

---

## References

[1] Van der Auwera GA et al. (2013). From FastQ data to high confidence variant calls: the Genome Analysis Toolkit best practices pipeline. *Current Protocols in Bioinformatics*. https://pmc.ncbi.nlm.nih.gov/articles/PMC4243306

[2] GATK Best Practices Workflows. Broad Institute. https://gatk.broadinstitute.org/hc/en-us/sections/360007226651-Best-Practices-Workflows

[3] Garrison E, Marth G (2012). Haplotype-based variant detection from short-read sequencing. arXiv:1207.3907. https://github.com/freebayes/freebayes

[4] FreeBayes GitHub repository. https://github.com/freebayes/freebayes

[5] Danecek P et al. (2021). Twelve years of SAMtools and BCFtools. *GigaScience* 10(2):giab008. https://github.com/samtools/bcftools

[6] BCFtools manual. https://samtools.github.io/bcftools/bcftools.html

[7] Frontiers in Bioinformatics (2025). Artificial intelligence in variant calling: a review. https://frontiersin.org/articles/10.3389/fbinf.2025.1574359/full

[8] Poplin R et al. (2018). Creating a universal SNP and small indel variant caller with deep neural networks. *Nature Biotechnology* 36:983–987. https://biorxiv.org/content/10.1101/092890v4.full.pdf

[9] DeepVariant GitHub. https://github.com/google/deepvariant

[10] Kolesnikov N et al. (2021). DeepTrio: variant calling in trios with deep learning. *Nature Biotechnology*.

[11] Bioinformatics (2023). Accelerated long-read variant calling with Clair3 for whole-genome sequencing. https://doi.org/10.1093/bioinformatics/btag181

[12] Zheng Z et al. (2022). Clair3: accurate long-read variant calling with pileup, full-alignment, and deep learning. *Nature Biotechnology*.

[13] Sentieon DNAscope documentation. https://www.sentieon.com

[14] PLOS ONE (2025). Variant calling in genomics: A comparative performance analysis and decision guide. https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0339891

[15] Briefings in Functional Genomics (2024). A comprehensive review of deep learning-based variant calling methods. https://doi.org/10.1093/bfgp/elae003

[16] Lin MF et al. (2018). Accurate, scalable cohort variant calls using DeepVariant and GLnexus. *Nature Biotechnology*. https://pmc.ncbi.nlm.nih.gov/articles/PMC8023681

[17] NVIDIA Parabricks documentation. https://docs.nvidia.com/clara/parabricks/tutorials/detailed-tutorials/wgs-variant-calling

[18] World Journal of Advanced Research and Reviews (2026). Exploring artificial intelligence for variant calling. https://wjarr.com/sites/default/files/fulltext_pdf/WJARR-2026-0877.pdf

[19] PMC (2021). Evaluation of serverless computing for scalable execution of a joint variant calling workflow. https://ncbi.nlm.nih.gov/pmc/articles/PMC8270184

[20] Self-Hosted Genomic Variant Calling: GATK vs FreeBayes vs BCFtools Compared. https://pistack.xyz/posts/2026-06-10-self-hosted-genomic-variant-calling-gatk-freebayes-bcftools

[21] Spheron Network (2026). NVIDIA Parabricks on GPU Cloud: 50x Faster Genomics Pipelines. https://spheron.network/blog/nvidia-parabricks-gpu-cloud-genomics-guide

[22] Journal of Genomic Medicine (2025). Cloud computing in population-scale genomics. https://doi.org/10.5734/jgm.2025.22.2.37

[23] Wang Group HPC Blog (2026). Estimating Computing Costs for Genomics Project Budgets. https://wanggroup.org/hpc/blog/budget-justification-2026

[24] PMC (2015). Scalable and cost-effective NGS genotyping in the cloud. https://pmc.ncbi.nlm.nih.gov/articles/PMC4608296

[25] PMC (2025). Celeste: A cloud-based genomics infrastructure with variant-calling pipeline suited for population-scale sequencing projects. https://pmc.ncbi.nlm.nih.gov/articles/PMC12060955

[26] NIH NSABB. Proposed Framework for the Oversight of Dual Use Life Sciences Research. https://osp.od.nih.gov/wp-content/uploads/Proposed-Oversight-Framework-for-Dual-Use-Research.pdf

[27] National Academies Press (2017). Dual Use Research of Concern in the Life Sciences. https://www.ncbi.nlm.nih.gov/books/NBK458495

[28] PMC (2018). Gene editing using CRISPR/Cas9: implications for dual-use and biosecurity. https://pmc.ncbi.nlm.nih.gov/articles/PMC5829273
