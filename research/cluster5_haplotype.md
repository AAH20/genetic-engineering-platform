# Cluster 5: Computational Genomics — Haplotype Inference

## Topic
Haplotype inference: computational methods, algorithms, scalability, and applications in genomic analysis.

## Summary
Haplotype inference encompasses two related problems: **haplotype assembly** (individual haplotyping from sequencing reads) and **haplotype phasing** (population-level inference from genotype data). Both are computationally challenging — the MEC (Minimum Error Correction) formulation of haplotype assembly is NP-hard, and population phasing scales super-linearly with sample size for most methods. Recent advances in long-read sequencing, quantum-inspired optimization, and PBWT-based algorithms are pushing the boundaries of accuracy and scalability.

---

## SOTA Approaches

1. **SHAPEIT4** — Sub-linear scaling with sample size using Positional Burrows-Wheeler Transform (PBWT) and Li-Stephens model; 1.6–11× faster than Beagle5/Eagle2/SHAPEIT3 on UK Biobank-scale data (10K–400K individuals). Memory: 30–52 GB depending on parameter P. [PMC6882857, Springer s41467-019-13225-y]

2. **QHap (Quantum-Inspired)** — Reformulates phasing as Max-Cut, solved via GPU-accelerated ballistic simulated bifurcation. 4–20× speedup over HapCUT2/WhatsHap on MHC region; 3–7× at chromosome scale. Pore-C integration boosts N50 by up to 15×. [arxiv.org/html/2603.25762v2]

3. **XHap (Transformer-based)** — Uses long-distance read correlations learned by transformers for haplotype assembly. Near-perfect reconstruction (CPR ≈ 1) at higher coverages; outperforms competing methods on multiple metrics. [doi.org/10.1093/bioadv/vbad169]

4. **HapCUT2** — Replaces MEC score with haplotype likelihood; enables assembly from long reads. Constructs read graph and seeks max-cut minimizing MEC. [Edge et al. 2017, cited in XHap paper]

5. **Beagle5 / Eagle2** — Linear or close-to-linear scaling with sample size; widely used for large-scale population phasing. [PMC6882857]

6. **WhatsHap** — Haplotype assembly from long reads; benchmarked against QHap and HapCUT2. [arxiv.org/html/2603.25762v2]

---

## NP-Hard Problems

1. **Minimum Error Correction (MEC)** — Proven NP-hard; even gapless MEC is NP-hard via reduction from MAX-CUT. UG-hard to compute O(1)-approximate solution. Best polynomial-time approximation has logarithmic performance guarantee. [Dagstuhl ESA 2018, PMC4393065]

2. **Single Individual Haplotyping (SIH)** — NP-hard even for reads of length 2. Binary matrix factorization formulation is NP-hard. [arxiv.org/pdf/1806.08647, PubMed 20529904]

3. **Haplotype phasing as Max-Cut** — Reformulation as Max-Cut problem is NP-hard, posing scalability challenge for population-scale phasing. [arxiv.org/html/2603.25762v2]

4. **General MEC with gaps** — NP-hard even when SNP matrix is gapless. [PMC4393065]

---

## Bottlenecks

1. **Read length limitation** — Short reads (<500 bp) often cover insufficient variants to fully phase haplotypes, resulting in fragmented blocks. Direct haplotyping restricted to ~600 bp with short-read sequencing. [PMC7731377]

2. **Scalability with sample size** — Most methods (Beagle5, Eagle2, SHAPEIT3) scale at best linearly with sample size. SHAPEIT4 achieves sub-linear scaling but requires 30–52 GB RAM. [PMC6882857]

3. **Memory requirements** — SHAPEIT3 requires 182.4 GB on 400K samples; SHAPEIT4-P=4 requires 52.3 GB; Beagle5 requires 47.3 GB. Large-scale phasing is memory-bound. [PMC6882857]

4. **Switch errors** — A single switch error inverts the entire downstream haplotype segment, breaking compound-heterozygote interpretation. Phasing contiguity varies with heterozygosity density. [zetobio.com blog]

5. **Block fragmentation** — Phased chromosomes break into blocks separated by unresolvable gaps; no reliable phase relationship between blocks. Block N50 varies multi-fold between populations. [zetobio.com blog]

6. **Polyploid assembly** — Haplotype assembly for polyploids (k>2) is more challenging than diploids; clustering reads into k groups becomes harder as ploidy grows. [XHap paper, doi.org/10.1093/bioadv/vbad169]

7. **Sequencing error rates** — Long-read technologies (ONT, PacBio) have higher error rates than short-read, complicating assembly. ONT not yet on par with short-read platforms for per-base accuracy. [PMC7731377]

8. **Pipeline idempotency failures** — Append-on-rerun, stale-output skip, and partial-write corruption are insidious failure modes in genomics pipelines that produce corrupted results with no error message. [nonstopio.com blog]

---

## Failure Modes

1. **Switch errors** — One wrong junction inverts all downstream alleles within a block; two pathogenic variants in trans can appear cis, breaking compound-heterozygote interpretation. [zetobio.com blog]

2. **Flip errors** — Single heterozygous site placed on wrong haplotype; more contained than switch errors but still corrupts variant interpretation. [zetobio.com blog]

3. **Block boundary failures** — Where reads don't bridge consecutive variants (low heterozygosity, repetitive regions, gaps longer than reads), phase linkage breaks and new block begins. [zetobio.com blog]

4. **Haplotype misclassification** — Statistical inference from multilocus genotypes is prone to misclassification; specific multilocus genotypes are consistently misclassified throughout entire datasets. [PLOS Genetics 10.1371/journal.pgen.0020127]

5. **Pipeline idempotency failures** — Three canonical modes: append-on-rerun (duplicate VCF headers), stale-output skip (empty/truncated output), partial-write corruption (temp file assumed valid). GATK HaplotypeCaller index desynchronization is especially vulnerable. [nonstopio.com blog]

6. **Four-gamete test failure** — Presence of all four haplotypes at two loci indicates recombination; failing this test enables exact phasing via Corners' Algorithm. [PMC9661815]

7. **Reference panel bias** — Phasing accuracy depends on reference panel composition; underrepresented populations may have higher switch error rates. [Nature Reviews Genetics s41576-025-00895-2]

---

## Cost Tradeoffs

1. **Molecular haplotyping vs. statistical inference** — Molecular haplotyping methods are expensive and not amenable to automation. Cost-benefit analysis shows power gain of LRTae over LRTstd varies with relative costs of genotyping, molecular haplotyping, and phenotyping. Greatest benefit when phenotyping cost is very high relative to genotyping (replication studies). [PubMed 16933998, PLOS Genetics 10.1371/journal.pgen.0020127]

2. **Short-read vs. long-read sequencing** — Short-read (Illumina) is state-of-the-art for SNV discovery but restricts direct haplotyping to ~600 bp. Long-read (ONT) enables direct haplotyping but has higher error rates. ONT MinION sequencer costs ~$1000; ~€20/sample with 96-sample multiplexing. [PMC7731377]

3. **10× Genomics linked-reads** — Provided additional phasing opportunities but required laborious/costly sample prep; product lines discontinued June 2020. [PMC7731377]

4. **Computational cost** — GATK HaplotypeCaller is computationally intensive; Rovaca achieves 57–76× speedup on standard CPUs. SHAPEIT4 reduces per-genome time with larger sample sizes. [biorxiv.org/2025.10.19.677660, PMC6882857]

5. **Hardware vs. software acceleration** — GPU/FPGA solutions (DeepVariant, DRAGEN) require specialized hardware; pure software solutions (Rovaca) democratize high-throughput analysis on commodity x86 CPUs. [biorxiv.org/2025.10.19.677660]

---

## Scalability Limits

1. **Sample size scaling** — SHAPEIT4 is the only method with sub-linear scaling; all others (Beagle5, Eagle2, SHAPEIT3) are linear or close-to-linear. At 400K samples, SHAPEIT4-P=4 is 4.1–11× faster than competitors. [PMC6882857]

2. **Memory scaling** — SHAPEIT3: 182.4 GB at 400K samples; SHAPEIT4-P=4: 52.3 GB; Beagle5: 47.3 GB; Eagle2: 8.8 GB. Memory is the primary constraint for million-sample datasets. [PMC6882857]

3. **Chromosome-scale phasing** — QHap read-based method approaches capacity constraints at chromosome scale (tens of thousands of nodes); SNP-based method scales with variant number rather than fragment number. [arxiv.org/html/2603.25762v2]

4. **Thread scaling** — Rovaca performance gains plateau beyond 50 threads while memory consumption continues to rise. [biorxiv.org/2025.10.19.677660]

5. **Long-read data volume** — SHAPEIT4 processes 2 Mb overlapping regions; memory usage varies with parameter P (P=1: 30.6 GB, P=4: 52.3 GB at 400K samples). [PMC6882857]

---

## Hardware Requirements

1. **Complete Genomics cWGS pipeline** — 48+ CPUs, 72+ GB RAM, ~1 TB storage per sample, 14 hours per sample analysis. [completegenomics.com]

2. **Rovaca variant caller** — Standard x86 CPU (Intel Xeon Gold 6248 @ 2.50 GHz), 384 GB RAM. No specialized hardware required. [biorxiv.org/2025.10.19.677660]

3. **SHAPEIT4** — 8.8–52.3 GB RAM depending on method and parameter settings; runs on standard Linux systems. [PMC6882857]

4. **ONT MinION** — $1000 instrument; Flongle flow cells for low-cost applications; 96-sample multiplexing achievable in single flow cell. [PMC7731377]

5. **QHap** — GPU-accelerated (ballistic simulated bifurcation solver); achieves 4–20× speedup over CPU-only methods. [arxiv.org/html/2603.25762v2]

---

## OSS Projects

1. **SHAPEIT4** — Open-source haplotype estimation; sub-linear scaling; integrates reference panels, long reads, pre-phased variants. [PMC6882857]

2. **HapCUT2** — Haplotype assembly from long reads; replaces MEC with haplotype likelihood. [Edge et al. 2017]

3. **Beagle5** — Linear-scale population phasing; widely used for large-scale datasets. [PMC6882857]

4. **Eagle2** — Fast phasing with 8.8 GB memory at 400K samples. [PMC6882857]

5. **WhatsHap** — Long-read haplotype assembly; benchmarked against QHap. [arxiv.org/html/2603.25762v2]

6. **Haplosaurus (Ensembl)** — Predicts whole-transcript haplotype sequences from phased genotypes; constructs haplotype pairs per transcript. [hub.docker.com/r/ensemblorg/ensembl-vep]

7. **HaploThread** — Desktop tool for haplotype network inference; C++/Qt; integrates McAN, fastHaN algorithms; GPL licensed. [doi.org/10.1093/molbev/msag052]

8. **Hapsolutely** — Reconstructs haplotypes and produces genealogy graphs from population data; Python/PyPI. [github.com/iTaxoTools/Hapsolutely]

9. **Rovaca** — Pure C++ variant caller; 57–76× faster than GATK HaplotypeCaller; open-source. [biorxiv.org/2025.10.19.677660]

10. **NGSEP** — Open-source Java package for variant discovery, genotyping, imputation. [discovery.researcher.life]

11. **XHap** — Transformer-based haplotype assembly using long-distance read correlations. [doi.org/10.1093/bioadv/vbad169]

12. **QHap** — Quantum-inspired haplotype phasing with GPU-accelerated bSB solver. [arxiv.org/html/2603.25762v2]

---

## Biosecurity Governance

1. **Invasive species biosecurity** — Haplotype analysis of mitochondrial D-loop used to identify mouse subspecies and VKORC1 mutations conferring rodenticide resistance. Biosecurity measures required to prevent introduction of resistant house mice. [PLOS One 10.1371/journal.pone.0236234]

2. **Crop biosecurity** — Haplotype diversity and LD analysis important for assessing genome manipulation approaches in soybean; wild relatives show greater genetic variability. [USDA ARS]

3. **Haplotype-based crop improvement** — Exploiting haplotype diversity for yield stability; prospective approaches involve resequencing large ancestral populations to identify haplotypes with broader variation. [Frontiers Plant Sci 10.3389/fpls.2017.01534]

4. **Quarantine and border control** — Haplotype networks used to trace origin of invasive populations; biosecurity checkpoints at state borders and airports. [PLOS One 10.1371/journal.pone.0236234]

5. **Compound heterozygosity and disease** — Haplotyping enables identification of compound heterozygous events; important for non-invasive prenatal genetic diagnostics and disease risk assessment. [XHap paper, doi.org/10.1093/bioadv/vbad169]

---

## Most Cited Papers

1. **"Advances in haplotype phasing and genotype imputation"** — Nature Reviews Genetics, 2025. Comprehensive review of phasing and imputation methods, practical QC considerations, long-read developments. [nature.com/articles/s41576-025-00895-2]

2. **"Accurate, scalable and integrative haplotype estimation" (SHAPEIT4)** — Nature Communications, 2019. Sub-linear scaling haplotype estimation; PBWT-based approach; benchmarked on UK Biobank. [PMC6882857, Springer s41467-019-13225-y]

3. **"Are Molecular Haplotypes Worth the Time and Expense?"** — PLOS Genetics, 2006. Cost-benefit analysis of molecular haplotyping; double-sampling approach for association studies. [PLOS Genetics 10.1371/journal.pgen.0020127]

4. **"A QPTAS for Gapless MEC"** — ESA 2018. Quasi-polynomial time approximation scheme for gapless MEC; partial settlement of approximation status. [Dagstuhl 10.4230/LIPIcs.ESA.2018.34]

5. **"Optimal algorithms for haplotype assembly from whole-genome sequence data"** — PubMed 20529904. Dynamic programming algorithm with O(m × 2^k × n) complexity; reduction to MAX-SAT.

6. **"Shape-IT: new rapid and accurate algorithm for haplotype inference"** — BMC Bioinformatics, 2008. Binary tree representation of candidate haplotypes; 50× faster than Phase v2.1. [PubMed 19087329]

7. **"XHap: haplotype assembly using long-distance read correlations learned by transformers"** — Bioinformatics Advances, 2023. Transformer-based assembly; near-perfect reconstruction at high coverage. [doi.org/10.1093/bioadv/vbad169]

8. **"A Long-Read Sequencing Approach for Direct Haplotype Phasing in Clinical Settings"** — PMC7731377. ONT-based clinical phasing; ~€20/sample with multiplexing.

9. **"QHap: Quantum-Inspired Haplotype Phasing"** — ArXiv 2026. GPU-accelerated bSB solver; 4–20× speedup over HapCUT2/WhatsHap. [arxiv.org/html/2603.25762v2]

10. **"Rovaca: A highly optimized variant caller"** — bioRxiv 2025. 57–76× faster than GATK HaplotypeCaller on standard CPUs. [biorxiv.org/2025.10.19.677660]

---

## Citations

- Nature Reviews Genetics: https://nature.com/articles/s41576-025-00895-2
- PMC Haplotype Applications: https://pmc.ncbi.nlm.nih.gov/articles/PMC12870298/
- Wiley Haplotype Inference Models: https://doi.org/10.1002/9780470892107.ch36
- ArXiv Matrix Completion SIH: https://arxiv.org/pdf/1806.08647
- XHap Transformer Assembly: https://doi.org/10.1093/bioadv/vbad169
- ScienceDirect SOM Haplotype: https://sciencedirect.com/science/article/pii/S0378475409000378
- Dagstuhl QPTAS Gapless MEC: https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ESA.2018.34
- IEEE Practical Exact MEC: https://www.computer.org/csdl/proceedings-article/bmei/2008/3118a072/12OmNALCNsH
- PMC HMEC Heuristic: https://pmc.ncbi.nlm.nih.gov/articles/PMC4393065
- PubMed Optimal Algorithms: https://pubmed.ncbi.nlm.nih.gov/20529904
- PubMed Shape-IT: https://pubmed.ncbi.nlm.nih.gov/19087329
- Brown Genome-wide Algorithms: https://cs.brown.edu/media/filer_public/c4/fe/c4fe43bb-1064-4f7d-85b7-7f6ea4edd75d/aguiar.pdf
- Ensembl VEP/Haplosaurus: https://hub.docker.com/r/ensemblorg/ensembl-vep
- HaploThread: https://doi.org/10.1093/molbev/msag052
- Hapsolutely: https://github.com/iTaxoTools/Hapsolutely
- Complete Genomics Hardware: https://www.completegenomics.com/learn/applications/complete-whole-genome-sequencing/
- Rovaca Variant Caller: https://biorxiv.org/content/10.1101/2025.10.19.677660v1.full-text
- PMC MEC Long Reads: https://pmc.ncbi.nlm.nih.gov/articles/PMC7292361/
- PubMed Cost-Effective Haplotypes: https://pubmed.ncbi.nlm.nih.gov/16933998/
- PMC Long-Read Clinical Phasing: https://pmc.ncbi.nlm.nih.gov/articles/PMC7731377/
- PLOS Genetics Cost-Benefit: https://journals.plos.org/plosgenetics/article?id=10.1371/journal.pgen.0020127
- PMC SHAPEIT4: https://pmc.ncbi.nlm.nih.gov/articles/PMC6882857
- ArXiv QHap: https://arxiv.org/html/2603.25762v2
- Springer SHAPEIT4: https://link.springer.com/article/10.1038/s41467-019-13225-y
- PLOS One Biosecurity: https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0236234
- USDA Soybean Haplotype: https://permanent.fdlp.gov/websites/www.ars.usda.gov/research/publications/publications.htm-SEQ_NO_115=135162.htm
- Frontiers Crop Haplotype: https://www.frontiersin.org/journals/plant-science/articles/10.3389/fpls.2017.01534/full
- Zetobio Phasing Limits: https://zetobio.com/blog/phasing-and-haplotype-assembly-limits-why-phased-has-a-resolution-you-rarely-see-reported
- PMC Four-Gamete Test: https://pmc.ncbi.nlm.nih.gov/articles/PMC9661815
- Nonstopio Idempotency: https://nonstopio.com/blogs/why-idempotency-is-underrated-in-genomics-pipeline-engineering
