# Cluster 5: Computational Genomics — Failure Modes

**Date:** 2026-10-04
**Search queries:** 10 (30 results total, top 3 per query)

---

## 1. Computational Genomics Failure Modes

| # | Finding | Source |
|---|---------|--------|
| 1 | Agentic LLMs evaluated by accuracy alone cannot reveal where in the workflow a failure originates; ClawBench attributes failures to architectural layers across variant calling and interpretation | [ClawBench (bioRxiv 2026)](https://biorxiv.org/content/10.64898/2026.06.30.735646v1.full-text) |
| 2 | AI coding agents cannot distinguish whether a failing test reflects a bug in their code or a bug in the test itself — documented across all 8 genomics modernization deployments | [AI Europe (2026)](https://europesays.com/ai/127904) |
| 3 | Planning errors, not execution faults, are the dominant failure mode in agentic bioinformatics; BioMaster/AutoBA/Biomni reached 87%/83%/70% pipeline completeness but plan correctness separated them more sharply | [Agentic AI in Bioinformatics (2026)](https://ampcome.com/post/agentic-ai-in-bioinformatics) |

## 2. Variant Calling Failure

| # | Finding | Source |
|---|---------|--------|
| 1 | GATK VariantFiltration: JEXL expressions with undefined variables (MQRankSum, ReadPosRankSum) silently skip filtering — variants that should fail the filter are marked PASS | [GATK Issue #8964](https://github.com/broadinstitute/gatk/issues/8964) |
| 2 | GATK4 HaplotypeCaller produces wrong genotype calls (heterozygous called as homozygous) and spurious insertions due to local realignment inside active regions; high depth (>1000x) impacts calls | [GATK Community](https://gatk.broadinstitute.org/hc/en-us/community/posts/360068136032-Multiple-cases-where-GATK4-is-not-giving-correct-variant-calls) |
| 3 | hap.py benchmarking tool: faulty variant test fails with "Cannot convert non-finite values (NA or inf) to integer" — unsupported REF alleles with undefined length cause installation failure | [Illumina/hap.py Issue #111](https://github.com/Illumina/hap.py/issues/111) |

## 3. Assembly Failure

| # | Finding | Source |
|---|---------|--------|
| 1 | GRC tracks 6 categories of assembly issues: Unknown, Clone Problem, Gap, Path Problem, Variation, Missing Sequence — mixed haplotypes and missing genes (e.g., TAS2R45) are common | [NCBI GRC](https://www.ncbi.nlm.nih.gov/grc/help/human-examples) |
| 2 | False gene and chromosome losses: thousands of genes completely or partially missing in previous Sanger-based and Illumina-based assemblies; many located in newly identified chromosomes | [Kim et al. 2022 (PMC9516821)](https://pmc.ncbi.nlm.nih.gov/articles/PMC9516821) |
| 3 | Genome assembly forensics (amosvalidate): automated pipeline for detecting large-scale mis-assemblies; Phrap tends to mis-assemble repetitive genomes; Celera Assembler produces fewer errors but still many in larger genomes | [Phillippy et al. 2008 (PMC2397507)](https://pmc.ncbi.nlm.nih.gov/articles/PMC2397507) |

## 4. MSA (Multiple Sequence Alignment) Failure

| # | Finding | Source |
|---|---------|--------|
| 1 | 5–90% of "homologous" residue pairs in reconstructed MSAs are erroneous depending on sequence divergence; three major causes: score-likelihood discrepancy, inadequate MSA space exploration, stochastic evolutionary processes | [Landan & Graur 2007 (PMC4799563)](https://ncbi.nlm.nih.gov/pmc/articles/PMC4799563) |
| 2 | Residue-pair error rates: ~5±2% (closely related) to 90±7% (distantly related); column error rate >50% for non-close sequences, rapidly reaching 100%; gapped columns have 79% error vs 47% for anchor columns | [Landan & Graur 2008 (PubMed 18614299)](https://pubmed.ncbi.nlm.nih.gov/18614299) |
| 3 | Systematic bias toward underestimation of gap count — reconstructed MSA is on average shorter than true MSA; correct reconstruction only guaranteed when true alignment likelihood is uniquely optimal (rarely the case) | [Landan & Graur 2009 PDF](http://nsmn1.uh.edu/dgraur/ArticlesPDFs/landan-graur-gene-2009.pdf) |

## 5. Failure in Open-Source Genomics Tools

| # | Finding | Source |
|---|---------|--------|
| 1 | 74% of research R scripts fail on first run in a clean computing environment; 57% of genomics tools fail when following their own documented installation instructions | [TechTimes (2026)](https://techtimes.com/articles/321880/20260728/ai-agents-rewrote-20000-lines-dead-genomics-code-scientists-still-checked-every-result.htm) |
| 2 | Silent tool failures: 91 validated cases where a tool call reported success while quietly dropping or corrupting data; 7 of 15 tools failed in >50% of test cases; ExpressionAtlas failed 75% of the time | [Silent Tool Failures (2026)](https://awesomeagents.ai/science/silent-tool-failures-causal-cot-just-in-time-memory) |
| 3 | AI agents rewriting genomics code: at ~90% parity, remaining divergences consisted of layered bugs stacking on each other; agent would revert its own work rather than push through failing tests | [AI Europe (2026)](https://europesays.com/ai/127904) |

## 6. Hardware Requirements & Failure

| # | Finding | Source |
|---|---------|--------|
| 1 | Cell Ranger: minimum 8-core AVX+ CPU, 64GB RAM, 1.5TB disk; large datasets (1M cells) require 32-core CPU, 512GB RAM, 2TB disk; AVX2 will be required in future | [10x Genomics](https://www.10xgenomics.com/support/software/cell-ranger/downloads/cr-system-requirements) |
| 2 | Space Ranger: minimum 8-core AVX CPU, 64GB RAM, 1TB disk; cluster mode requires NFS + Slurm; default ulimits (1024–4096 open files/processes) too low for multi-core jobs | [10x Genomics](https://www.10xgenomics.com/support/software/space-ranger/downloads/space-ranger-system-requirements) |
| 3 | Hardware acceleration challenges: short read alignment is principal computational bottleneck; NoC routing constraints cause idle computation units and high latency; irregular traffic patterns from repeated memory accesses | [Robinson et al. 2021 (PMC8317111)](https://pmc.ncbi.nlm.nih.gov/articles/PMC8317111) |

## 7. Cost Analysis & Failure

| # | Finding | Source |
|---|---------|--------|
| 1 | Medicare rebates for genomic sequencing cover only 21–63% of microcosting-estimated economic cost; labs may not offer tests due to financial viability | [Genetics in Medicine (2024)](https://gimjournal.org/article/S1098-3600(24)00244-2/pdf) |
| 2 | 15–40% of pipeline runs hit at least one failure and restart; 25% failure rate creates 25% hidden markup ($9→$11.25/sample); 2,000 samples/month = $54,000/year wasted compute | [The Register (2026)](https://theregister.com/cloud/2026/06/11/cost-per-genomics-sample-try-cost-per-sequencing-attempt/5254177) |
| 3 | Storage retrieval hidden costs: 30GB compressed → 200GB uncompressed; decompression failures when disk/memory not sized; somatic (60–100x depth) generates 600GB FASTQ files | [The Register (2026)](https://theregister.com/cloud/2026/06/11/cost-per-genomics-sample-try-cost-per-sequencing-attempt/5254177) |

## 8. Scalability Failure

| # | Finding | Source |
|---|---------|--------|
| 1 | Scalable Genomics (founded 2009, NYC) — deadpooled; cloud-based genomics analysis SaaS failed to achieve sustainable scale | [Tracxn](https://platform.tracxn.com/a/d/company/58bd18e1e4b041de9c7ce81c/scalable%20genomics) |
| 2 | GPU scaling: >200-fold runtime decrease, ~5–10-fold cost reduction vs CPUs using PyTorch/TensorFlow; current methods handle tens–thousands of samples but need to scale to millions | [Taylor-Weiner et al. 2019 (Genome Biol)](https://www.broadinstitute.org/publications/broad625196) |
| 3 | Genomic datasets double every ~8 months, far exceeding Moore's law; typical whole genome BAM >100GB; "In many cases, it's between a computation taking a second, a day, or never completing at all" | [Broad Institute Blog](https://www.broadinstitute.org/blog/harnessing-flood-scaling-data-science-big-genomics-era) |

## 9. Biosecurity Failure

| # | Finding | Source |
|---|---------|--------|
| 1 | Crop biosecurity: genomic information available for only a few plant-associated microbes, few of which are highest-risk; $500M over 5 years needed for just 9 targeted pathogens vs $20–33B annual losses | [APS White Paper](https://www.apsnet.org/members/engagement/ppb/Documents/CropBiosecurityWhitePaper5-03.pdf) |
| 2 | Beacon Project security hole: individual genome identifiable within beacon network using just 5,000 queries; de-identification insufficient; recommended fixes: ban anonymous queries, merge datasets, require approval, limit genomic regions | [Stanford Medicine (2015)](https://med.stanford.edu/news/all-news/2015/10/stanford-researchers-identify-potential-security-hole-in-genomic.html) |
| 3 | Synthetic biology biosecurity: low-to-medium awareness among practitioners; most effective intervention point is at DNA synthesis level (gene-synthesis firms); need harmonized screening strategies, central virulence factor database | [Kelle 2008 (PMC2725994)](https://pmc.ncbi.nlm.nih.gov/articles/PMC2725994) |

## 10. NP-Hard Problems in Computational Genomics

| # | Finding | Source |
|---|---------|--------|
| 1 | NP-hard problems surveyed across genome comparison/completion, sequence assembly/analysis, haplotyping, and phylogenetics; parameterized algorithms exploit "law of low real-world complexity" | [Algorithms 2019](https://doi.org/10.3390/a12120256) |
| 2 | Shortest Common Superstring (SCS) is NP-complete; genome assembly via de Bruijn graphs is NP-hard by reduction from SCS; string-graph model NP-hard by reduction from Hamiltonian cycle; practical instances solvable due to heavy oversampling (large σ regime) | [Phys Rev E 2024](https://link.aps.org/doi/10.1103/PhysRevE.109.014133) |
| 3 | Covering alignment of labeled DAGs (pan-genome graphs) is NP-hard even on binary alphabets; recombination-oblivious diploid alignment NP-hard for alphabet size ≥2; phase transition between polynomial and NP-hard alignment | [arXiv 1611.05086](https://ar5iv.labs.arxiv.org/html/1611.05086) |

---

## Synthesis: Key Bottlenecks

1. **Alignment bottleneck**: Short read alignment is the principal computational bottleneck in every genomics pipeline; hardware acceleration (GPU/FPGA/NoC) faces memory access and routing constraints
2. **Error propagation**: MSA errors (5–90% erroneous residue pairs) propagate to all downstream analyses; variant calling errors (wrong genotypes, spurious indels) propagate through clinical interpretation
3. **Silent failures**: Tools report success while dropping/corrupting data (91 validated cases); pipeline failures (15–40%) are invisible in cost-per-sample metrics
4. **Scalability gap**: Data doubles every 8 months, exceeding Moore's law; current methods handle thousands of samples but need millions
5. **Reproducibility crisis**: 74% of R scripts fail on first run; 57% of genomics tools fail following their own installation docs
6. **NP-hard barriers**: Assembly, pan-genome alignment, and haplotyping are fundamentally NP-hard; practical solutions rely on oversampling and parameterized complexity

## Most Cited Papers

- Landan & Graur (2007/2008) — MSA error characterization
- Phillippy, Schatz & Pop (2008) — Genome assembly forensics
- Taylor-Weiner et al. (2019) — GPU scaling for genomics
- Kim et al. (2022) — False gene/chromosome losses in assemblies
- Robinson et al. (2021) — Hardware acceleration challenges
- Garfinkel et al. (2007) — Synthetic genomics governance
- Shringarpure & Bustamante (2015) — Beacon Project security hole
