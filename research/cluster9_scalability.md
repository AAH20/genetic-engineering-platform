# Cluster 9: AI/ML for Genomics — Scalability Research

**Date:** 2026-10-04
**Focus:** Scalability of AI/ML approaches in genomics

---

## 1. AI/ML for Genomics Scalability

### Top Results

1. **NHGRI Fact Sheet: Artificial Intelligence, Machine Learning and Genomics** — Genomics research will generate 2–40 exabytes of data within the next decade. AI/ML tools are needed to handle, extract, and interpret this data. Applications include facial analysis for genetic disorder identification, liquid biopsy cancer classification, cancer progression prediction, variant pathogenicity classification, and CRISPR gene editing optimization. NHGRI's Genomic Data Science Working Group collaborates with NIH to define critical areas for AI/ML in genomics. [https://www.genome.gov/about-genomics/educational-resources/fact-sheets/artificial-intelligence-machine-learning-and-genomics](https://www.genome.gov/about-genomics/educational-resources/fact-sheets/artificial-intelligence-machine-learning-and-genomics)

2. **Malin: Challenges and Opportunities for Machine Learning in Genomics** — Key challenges include: need for diverse big data, cost-effective storage and compute, trust through bringing the learn to the data, explainable findings for clinical use, verifiable and auditable decision support tied to algorithm versions, equitable accessibility, and secure multiparty computation for encrypted genomic data. [https://www.genome.gov/sites/default/files/media/files/2021-04/Malin_Genomic_Challenges_v2.pdf](https://www.genome.gov/sites/default/files/media/files/2021-04/Malin_Genomic_Challenges_v2.pdf)

3. **GenoML** — Automated machine learning platform for genomics that streamlines data analysis, optimizes ML pipelines, and accelerates discovery. [https://genoml.com](https://genoml.com)

### Synthesis

The scalability challenge in genomics AI/ML is fundamentally a data problem: 2–40 exabytes of genomic data will be generated within a decade. Current bottlenecks include the need for diverse training data (most genomic data comes from European-ancestry populations), cost-effective storage and compute infrastructure, and the "last mile" problem of moving ML models into clinical practice with explainability and auditability. The field requires bringing computation to data (federated learning, secure multiparty computation) rather than centralizing sensitive genomic data.

---

## 2. Protein Language Model Scalability

### Top Results

1. **Reverse Distillation: Consistently Scaling Protein Language Model Representations** — Unlike NLP/CV, protein language models (PLMs) scale poorly: models within the same family plateau or decrease in performance, with mid-sized models often outperforming the largest. Reverse Distillation decomposes large PLM representations into orthogonal subspaces guided by smaller models, creating a Matryoshka-style nested structure. On ProteinGym benchmarks, reverse-distilled ESM-2 variants outperform baselines at the same embedding dimensionality, with the 15B parameter model achieving strongest performance. [https://arxiv.org/pdf/2603.07710v1](https://arxiv.org/pdf/2603.07710v1)

2. **Training Compute-Optimal Protein Language Models** — Scaling laws for PLMs differ from NLP: training data scales sublinearly with model size but follows distinct power-laws. A 10× increase in compute leads to 6× increase in MLM model size and 70% increase in data, versus 4× model size and 3× training tokens for CLM. Protein sequences (20 amino acids, little redundancy) are a distinct modality from natural language. [https://arxiv.org/html/2411.02142](https://arxiv.org/html/2411.02142)

3. **Scaling and Data Saturation in Protein Language Models** — No evidence of model saturation on protein function prediction: performance improves (non-monotonically) with added data from UniRef100 yearly snapshots (2011–2024). Unsupervised predictions improve year-over-year but do not yet consistently outperform supervised baselines. [https://arxiv.org/pdf/2507.22210v1](https://arxiv.org/pdf/2507.22210v1)

### Synthesis

Protein language models face a unique scaling challenge: unlike NLP where scaling laws are predictable, PLMs exhibit non-monotonic scaling behavior where mid-sized models often outperform larger ones. This is attributed to the low redundancy of protein sequences (20 amino acid vocabulary vs. natural language's semantic smoothness). The Reverse Distillation framework addresses this by creating orthogonal subspaces that prevent destructive interference between features at different scales. Compute-optimal training requires balancing model parameters and data differently than NLP — data scales sublinearly with model size.

---

## 3. Variant Effect Prediction Scalability

### Top Results

1. **Sequence UNET: High-throughput Deep Learning Variant Effect Prediction** — A fully convolutional architecture that classifies and predicts variant frequency from sequence alone. Analyzed 8.3 billion variants in 904,134 proteins. Runs on modest hardware: 1.5h on GPU (batch size 100), 6.8h without batching, 50.9h CPU-only. Comparable pathogenicity prediction to ESM-1b but with far greater scalability. [https://link.springer.com/article/10.1186/s13059-023-02948-3](https://link.springer.com/article/10.1186/s13059-023-02948-3)

2. **Fine-tuning PLMs with Deep Mutational Scanning for Variant Effect Prediction** — NLR (Normalised Log-odds Ratio) fine-tuning of ESM-1v on DMS data improves missense variant effect predictions across ProteinGym and ClinVar benchmarks. Consistent improvements across all benchmarks, proteins, and ESM models. AlphaMissense achieves SOTA on multiple tasks. [https://arxiv.org/html/2405.06729v1](https://arxiv.org/html/2405.06729v1)

3. **A Scalable Approach to Resolving Variants of Uncertain Significance** — Over 90% of missense variants across ~4,000 disease-associated genes are VUS. A scalable workflow using experimental and predictive evidence reclassified 75% of 16,115 VUS as pathogenic or benign with <1% error. Analyzed >90,000 unobserved variants; 62% had enough evidence for preclassification. [https://pubmed.ncbi.nlm.nih.gov/41727046](https://pubmed.ncbi.nlm.nih.gov/41727046)

### Synthesis

Variant effect prediction scalability has been addressed through two complementary approaches: (1) efficient architectures like Sequence UNET that use fully convolutional networks to achieve proteome-scale predictions (8.3B variants in hours), and (2) fine-tuning large PLMs on experimental DMS data to improve accuracy. The VUS problem remains the dominant clinical challenge — over 90% of missense variants in disease genes lack clinical interpretation. Scalable evidence generation combining multiplexed assays, arrayed assays, and computational predictions can resolve most VUS with <1% error.

---

## 4. Drug-Target Interaction (DTI) Prediction Scalability

### Top Results

1. **Komet: Drug-Target Interactions Prediction at Scale** — A Kronecker Optimized METhod using Nyström approximation for scalable DTI prediction. Three-step framework with efficient computation for large datasets. LCIdb dataset provides extensive coverage of molecule and druggable protein spaces. GPU-parallel computation, superior scalability vs. deep learning approaches. [https://biorxiv.org/content/10.1101/2024.02.22.581599v4.full-text](https://biorxiv.org/content/10.1101/2024.02.22.581599v4.full-text)

2. **LinkD: Unified Agent-Enabled Platform for Drug Repurposing** — Combines structure-informed latent diffusion DTI prediction with entropy-aware selectivity scoring, cellular phenotype validation, and clinical evidence from 11.5M individuals' EHRs. LinkD-DTI ranks first on 8 of 9 benchmarks. [https://biorxiv.org/content/biorxiv/early/2026/04/22/2026.04.19.719462.full.pdf](https://biorxiv.org/content/biorxiv/early/2026/04/22/2026.04.19.719462.full.pdf)

3. **Komet (ACS JCIM)** — Published version confirming Komet's scalability advantages: competes with or outperforms SOTA deep learning on medium datasets but scales much better to very large datasets in computation time and memory. [https://pubs.acs.org/doi/pdf/10.1021/acs.jcim.4c00422](https://pubs.acs.org/doi/pdf/10.1021/acs.jcim.4c00422)

### Synthesis

DTI prediction scalability requires both large high-quality training datasets (LCIdb) and algorithms that can scale to those datasets (Komet's Kronecker structure with Nyström approximation). The field is moving toward multi-scale integration: combining molecular DTI predictions with cellular phenotype data and clinical EHR evidence. GPU parallel computation is essential for handling the combinatorial explosion of molecule-protein pairs.

---

## 5. Scalability Open Source Tools

### Top Results

1. **GATK4 (Broad Institute)** — Fully open-source (BSD 3-clause) genome variant discovery package. Covers all major variant classes (SNPs, indels, CNV, SV) for germline and cancer. Intel collaboration rewrote core code for performance, flexibility, speed, and scalability. GenomicsDB datastore dramatically improved joint-calling pipeline scalability. Includes ML-based tools (CNN for variant filtering). [https://www.broadinstitute.org/news/broad-institute-releases-open-source-gatk4-software-genome-analysis-optimized-speed-and](https://www.broadinstitute.org/news/broad-institute-releases-open-source-gatk4-software-genome-analysis-optimized-speed-and)

2. **GenomeTools** — Versatile open-source genome analysis software including Tallymer (memory-efficient k-mer counting for large sequence sets), Readjoiner (fast memory-efficient string graph assembler), and LTRdigest (automated LTR retrotranson annotation). [https://genometools.org/](https://genometools.org/)

3. **Scalable Genomics** — Stealth-mode bioinformatics company developing plug-and-play analysis of genome sequencing data using cloud computing and virtualization for clinical, environmental, research, and forensic samples. [https://scalablegenomics.com](https://scalablegenomics.com)

### Synthesis

The open-source genomics ecosystem has matured significantly. GATK4 represents the gold standard for variant discovery with its Intel-optimized core and GenomicsDB for scalable joint calling. GenomeTools provides foundational data structures for memory-efficient sequence analysis. The trend is toward cloud-native, containerized pipelines that can scale elastically. NVIDIA Parabricks provides GPU-accelerated implementations of standard tools (BWA-MEM2, DeepVariant) with 10-20× speedups.

---

## 6. Scalability Hardware Requirements

### Top Results

1. **HCLS AI Factory White Paper** — End-to-end platform on NVIDIA DGX Spark ($4,699 desktop workstation with GB10 GPU, 128GB unified memory). Processes 200GB FASTQ → 100 drug candidates in <5 hours. Parabricks: BWA-MEM2 alignment 20-45 min, DeepVariant 10-35 min (10-20× CPU speedup). Scales to DGX SuperPOD for enterprise. [https://hcls-ai-factory.org/HCLS_AI_FACTORY_WHITE_PAPER_DGX_SPARK](https://hcls-ai-factory.org/HCLS_AI_FACTORY_WHITE_PAPER_DGX_SPARK)

2. **NVIDIA Parabricks Hardware Requirements** — Supports CUDA 75-120 GPUs with ≥16GB VRAM. Tested on T4, A10, A30, A40, A100, A6000, L4, L40, H100, H200, GH200, B200, B300, GB200, GB300, RTX PRO 6000/4500, DGX Spark/Station. CPU RAM scales with GPU count: 2 GPUs → 100GB RAM, 4 → 196GB, 8 → 392GB. [https://github.com/NVIDIA-AI-Blueprints/genomics-analysis](https://github.com/NVIDIA-AI-Blueprints/genomics-analysis)

3. **Nucleotide Transformer Fine-tuning with NeMo** — Requires high-performance GPU (A100 or equivalent, ≥40GB VRAM) for 2.5B parameter model. Uses Megatron-Core for distributed architectures even on single GPU. [https://medium.com/@frankmorales_91352/bridging-the-scale-gap-a-tutorial-on-fine-tuning-the-nucleotide-transformer-with-nvidia-nemo-2-6-1-61d792080f04](https://medium.com/@frankmorales_91352/bridging-the-scale-gap-a-tutorial-on-fine-tuning-the-nucleotide-transformer-with-nvidia-nemo-2-6-1-61d792080f04)

### Synthesis

Hardware requirements span a wide range: from $4,699 DGX Spark desktop workstations for proof-of-concept to DGX SuperPOD for enterprise-scale deployment. GPU acceleration is essential — CPU-based BWA-MEM takes 12-24 hours vs. 20-45 minutes on GPU. The minimum viable GPU configuration is 16GB VRAM (T4-class), but serious training requires A100/H100-class GPUs with 40-80GB+ VRAM. CPU RAM requirements scale linearly with GPU count (50GB per GPU). The convergence of genomics and drug discovery on a single GPU platform is a key enabler.

---

## 7. Scalability Cost Analysis

### Top Results

1. **Microsoft Azure Genomics Pricing** — Azure offers scalable, secure genomics secondary analysis from raw reads to variant calls. Pay-per-use model with cloud elasticity. [https://azure.microsoft.com/en-us/pricing/details/genomics](https://azure.microsoft.com/en-us/pricing/details/genomics)

2. **Benchmarking Undedicated Cloud Computing for Genomic Analysis** — GCE outperformed EMR in cost and wall-clock time. For ~36× coverage human genome at ~$1,000 sequencing cost: GCE computation median $29.81, EMR $69.60. EMR was 257.3% (E.coli) and 173.9% (human) more expensive than GCE. [https://pmc.ncbi.nlm.nih.gov/articles/PMC4172764](https://pmc.ncbi.nlm.nih.gov/articles/PMC4172764)

3. **GenoML** — Automated ML platform aiming to reduce cost and streamline genomics analysis pipelines. [https://genoml.com](https://genoml.com)

### Synthesis

Cloud computing is cost-effective for genomics: computation costs ($30-70 per human genome) are now a small fraction of sequencing costs (~$1,000). However, provider choice matters significantly — GCE was 60-70% cheaper than EMR in benchmarks. The trend is toward serverless, containerized pipelines that scale elastically. GPU-accelerated cloud instances (A100/H100) are cost-effective for training large models but expensive for inference. The total cost of ownership must include data transfer, storage, and the hidden costs of pipeline orchestration and monitoring.

---

## 8. Scalability Biosecurity

### Top Results

1. **Governing Synthetic Biology and AI Convergence: Biosecurity Priorities for Africa** — AI-driven SynBio increases ease of cyber-biothreats (weaponization by corruption and denial). AI tools using LLMs for protein/genome design can speed up design-build-test-learn cycle, raising concerns about pathogen-related research. Current frameworks (BWC, WHO, GHSA) focus on physical biological weapons, not intangible AI/SynBio tools. Proposes embedding AI considerations in biosafety processes, proportionate risk-based oversight, and DNA synthesis screening. [https://frontiersin.org/journals/bioengineering-and-biotechnology/articles/10.3389/fbioe.2026.1834976/full](https://frontiersin.org/journals/bioengineering-and-biotechnology/articles/10.3389/fbioe.2026.1834976/full)

2. **Securing Dual-Use Pathogen Data of Concern** — Five-tier Biosecurity Data Level (BDL) framework for categorizing pathogen data by risk. Proposes technical restrictions per tier. Trusted Research Environments (TREs) with: risk-tiered data classification, locked-down compute (isolated VMs, no inbound internet), strong identity/training/contracting, and egress control with biosecurity checks. Over 100 researchers endorsed data controls at Asilomar. [https://arxiv.org/pdf/2602.08061](https://arxiv.org/pdf/2602.08061)

3. **From Capability Uplift to Capability Governance: An AI-Biosecurity Stack** — Risk emerges from connections among data, models, agents, lab automation, synthesis access, experimental validation, and governance. If-then strategy links observable developments to capability assessments. Governance should be capability-based, not label-based. Build-test stages remain a bottleneck. [https://frontiersin.org/articles/10.3389/fmicb.2026.1899413/full](https://frontiersin.org/articles/10.3389/fmicb.2026.1899413/full)

### Synthesis

Biosecurity governance has not kept pace with AI-SynBio convergence. The core tension: open data and open models drive science but also enable misuse. The BDL framework proposes tiered data access with technical controls. Key governance gaps: fragmented institutional mandates, uneven regulatory capacity, dependence on external infrastructure, and limited AI literacy in biosafety systems. The capability stack model recognizes that risk emerges from the entire pipeline (data → models → agents → lab automation → synthesis), not any single component. DNA synthesis screening is a critical chokepoint.

---

## 9. Scalability Failure Modes

### Top Results

1. **ClawBench: Benchmarking LLMs for ACMG/AMP Variant Interpretation** — Dangerous misclassification (benign↔pathogenic) is rare (0.3-2.2%) and model-invariant — a property of pipeline architecture, not the model. Different variant classes are rate-limited by different layers: LoF by combiner threshold, rare missense by evidence formation. Fabricated evidence is measurable and neutralized by execution. Trustworthiness is a property of pipeline architecture, not the model. [https://biorxiv.org/content/10.64898/2026.06.30.735646v1.full.pdf](https://biorxiv.org/content/10.64898/2026.06.30.735646v1.full.pdf)

2. **AI Coding Agents in Genomics Pipelines** — 60.2× speedup in RNA-seq QC, Rust rewrite of 20,000-line genome aligner matching 99.815% of reads. BUT: agents cannot determine whether a failing test reflects a bug in their code or the test itself. "Eloquent, convincing, and confidently wrong in ways that are easy to miss." Silent failures: inverted control parameters, incorrectly scaled correction factors. [https://bizstack.tech/ai-coding-agents-hit-60x-speedups-but-cant-validate-their-own-output](https://bizstack.tech/ai-coding-agents-hit-60x-speedups-but-cant-validate-their-own-output)

3. **Agentic Genomics Verification** — Bottleneck has moved from constructing analyses to validating them. Characteristic danger: silent degradation to plausible-looking but incorrect results. Examples: pharmacogenomic skill returning "all-normal" from empty input, mixing GRCh37/GRCh38 coordinates, out-of-distribution tool runs. Structural failures (reference mixing, missing preconditions, scope violations) can be made unrepresentable through typed contracts. [https://eigenius.online/articles/agentic-genomics-verification](https://eigenius.online/articles/agentic-genomics-verification)

### Synthesis

The dominant failure mode in scalable genomics AI is **silent degradation** — plausible-looking but incorrect results that pass validation. Key failure categories: (1) dangerous misclassification (rare but clinically critical), (2) fabricated evidence from LLMs, (3) reference genome mixing (GRCh37/GRCh38), (4) empty-input precondition violations, (5) out-of-distribution application, (6) cross-skill composition failures. The insight from ClawBench is that trustworthiness is a property of pipeline architecture, not the model — fail-closed evidence contracts and validated execution are essential. Structural failures can be eliminated through typed contracts at skill interfaces.

---

## 10. Scalability NP-Hard Problems

### Top Results

1. **Hardness of Covering Alignment: Phase Transition in Post-Sequence Genomics** — Finding a covering alignment of two labeled DAGs is NP-hard even on binary alphabets. Comparing two pan-genome representations is NP-hard. Phase transition: k=1 is NP-hard, k=2 is classical quadratic-time sequence alignment. Diploid alignment (recombination-oblivious) is NP-hard on alphabets of size ≥2. [https://ar5iv.labs.arxiv.org/html/1611.05086](https://ar5iv.labs.arxiv.org/html/1611.05086)

2. **Parameterized Algorithms in Bioinformatics** — Survey of NP-hard problems in genome comparison, sequence assembly, haplotyping, and phylogenetics. DCJ distance is NP-hard in unsigned permutation model. Parameterized complexity exploits "law of low real-world complexity" — biological data is structured and governed by simple processes. [https://doi.org/10.3390/a12120256](https://doi.org/10.3390/a12120256)

3. **Phase Transition in Computational Complexity of Shortest Common Superstring and Genome Assembly** — SCS is NP-complete. Genome assembly via de Bruijn graphs is NP-hard by reduction from SCS. String-graph model is NP-hard by reduction from Hamiltonian cycle. BUT: practical instances are deep in the "easy phase" due to heavy oversampling (high coverage). Polynomial-time solvable in the large-coverage regime. [https://pubmed.ncbi.nlm.nih.gov/38366408](https://pubmed.ncbi.nlm.nih.gov/38366408)

### Synthesis

Many fundamental genomics problems are NP-hard: pan-genome comparison, diploid alignment, sequence assembly (SCS), and various genome rearrangement distances. However, the "law of low real-world complexity" means practical instances are often tractable through parameterized algorithms. The phase transition framework shows that genome assembly is tractable in the high-coverage regime (which modern sequencing provides). The key insight is that biological data has structure (low complexity) that pathological NP-hard instances lack. Pan-genome analysis is the emerging frontier where NP-hardness becomes practically relevant.

---

## Cross-Cutting Synthesis

### Key Bottlenecks

1. **Data diversity and bias**: Most genomic data is from European-ancestry populations, limiting model generalizability
2. **Compute infrastructure**: Training large PLMs requires A100/H100-class GPUs; inference at scale requires GPU acceleration
3. **Storage and data transfer**: 2-40 exabytes of genomic data will be generated; data gravity is a major challenge
4. **Clinical translation gap**: Moving from research-grade to clinical-grade requires explainability, auditability, and regulatory approval
5. **VUS resolution**: >90% of missense variants in disease genes lack clinical interpretation
6. **Silent failure modes**: Plausible-looking but incorrect results that pass validation
7. **Biosecurity governance**: Frameworks have not kept pace with AI-SynBio convergence

### Scalability Strategies

1. **Algorithmic efficiency**: Convolutional architectures (Sequence UNET), Kronecker methods (Komet), Nyström approximation
2. **Model compression**: Reverse Distillation for PLMs, knowledge distillation
3. **Hardware acceleration**: GPU-accelerated pipelines (Parabricks, 10-20× speedup)
4. **Cloud elasticity**: Containerized, serverless pipelines that scale on demand
5. **Federated approaches**: Bringing computation to data (secure multiparty computation)
6. **Typed contracts**: Making structural failures unrepresentable at skill interfaces

### Cost Trade-offs

- **Cloud vs. on-premises**: Cloud offers elasticity but data transfer costs are significant; on-premises offers control but limited scalability
- **CPU vs. GPU**: GPU essential for training and alignment; CPU sufficient for some inference tasks
- **Model size vs. performance**: Mid-sized models often outperform larger ones in PLMs; compute-optimal scaling requires balancing parameters and data
- **Open-source vs. commercial**: Open-source (GATK4, GenomeTools) offers transparency; commercial (Parabricks, Azure Genomics) offers support and integration

### Hardware Requirements Summary

| Use Case | Minimum GPU | Recommended GPU | RAM |
|----------|-------------|-----------------|-----|
| Variant calling (Parabricks) | 16GB VRAM (T4) | 48GB VRAM (L40S) | 100-392GB |
| PLM training (2.5B) | 40GB VRAM (A100) | 80GB+ VRAM (H100) | 500GB+ |
| DTI prediction | 16GB VRAM | 40GB+ VRAM | 100GB+ |
| End-to-end pipeline | DGX Spark ($4,699) | DGX SuperPOD | 128GB+ |

### Biosecurity Governance Priorities

1. Tiered data access (BDL framework) with technical controls
2. DNA synthesis screening as a critical chokepoint
3. Capability-based governance (not label-based)
4. Continuous assessment (not one-time review)
5. Institutional integration of AI literacy in biosafety
6. Proportionate, risk-based oversight

### Failure Mode Taxonomy

| Failure Mode | Category | Mitigation |
|-------------|----------|------------|
| Dangerous misclassification | Clinical | Fail-closed evidence contracts |
| Fabricated evidence | LLM hallucination | Validated execution |
| Reference mixing | Structural | Typed coordinates (assembly-aware) |
| Empty-input violations | Precondition | Input contracts |
| Out-of-distribution | Scope | Validated population metadata |
| Cross-skill composition | Seam | Typed I/O contracts |

### NP-Hard Problems in Genomics

| Problem | Complexity | Practical Tractability |
|---------|-----------|----------------------|
| Pan-genome comparison | NP-hard | Parameterized algorithms |
| Diploid alignment | NP-hard | Heuristics |
| Sequence assembly (SCS) | NP-hard | Easy phase (high coverage) |
| DCJ distance (unsigned) | NP-hard | FPT algorithms |
| Shortest common superstring | NP-complete | Polynomial in high-coverage regime |

---

## Citations

1. NHGRI. "Artificial Intelligence, Machine Learning and Genomics." https://www.genome.gov/about-genomics/educational-resources/fact-sheets/artificial-intelligence-machine-learning-and-genomics
2. Malin, B. "Challenges and Opportunities for Machine Learning in Genomics." https://www.genome.gov/sites/default/files/media/files/2021-04/Malin_Genomic_Challenges_v2.pdf
3. GenoML. https://genoml.com
4. "Reverse Distillation: Consistently Scaling Protein Language Model Representations." arXiv:2603.07710v1. https://arxiv.org/pdf/2603.07710v1
5. "Training Compute-Optimal Protein Language Models." arXiv:2411.02142. https://arxiv.org/html/2411.02142
6. "Scaling and Data Saturation in Protein Language Models." arXiv:2507.22210v1. https://arxiv.org/pdf/2507.22210v1
7. "High-throughput deep learning variant effect prediction with Sequence UNET." Genome Biology, 2023. https://link.springer.com/article/10.1186/s13059-023-02948-3
8. "Fine-tuning protein language models with deep mutational scanning improves variant effect prediction." arXiv:2405.06729v1. https://arxiv.org/html/2405.06729v1
9. "A scalable approach to resolving variants of uncertain significance." PubMed, 2026. https://pubmed.ncbi.nlm.nih.gov/41727046
10. "Drug-Target Interactions Prediction at Scale: the Komet Algorithm with the LCIdb Dataset." bioRxiv, 2024. https://biorxiv.org/content/10.1101/2024.02.22.581599v4.full-text
11. "A Unified Agent-Enabled Platform for Drug Repurposing." bioRxiv, 2026. https://biorxiv.org/content/biorxiv/early/2026/04/22/2026.04.19.719462.full.pdf
12. "Komet: Drug-Target Interactions Prediction at Scale." JCIM, 2024. https://pubs.acs.org/doi/pdf/10.1021/acs.jcim.4c00422
13. "Broad Institute releases open-source GATK4." https://www.broadinstitute.org/news/broad-institute-releases-open-source-gatk4-software-genome-analysis-optimized-speed-and
14. GenomeTools. https://genometools.org/
15. Scalable Genomics. https://scalablegenomics.com
16. "HCLS AI Factory White Paper." https://hcls-ai-factory.org/HCLS_AI_FACTORY_WHITE_PAPER_DGX_SPARK
17. "NVIDIA Parabricks Hardware Requirements." https://github.com/NVIDIA-AI-Blueprints/genomics-analysis
18. "Bridging the Scale-Gap: Fine-Tuning the Nucleotide Transformer with NVIDIA NeMo 2.6.1." https://medium.com/@frankmorales_91352/bridging-the-scale-gap-a-tutorial-on-fine-tuning-the-nucleotide-transformer-with-nvidia-nemo-2-6-1-61d792080f04
19. "Microsoft Azure Genomics Pricing." https://azure.microsoft.com/en-us/pricing/details/genomics
20. "Benchmarking Undedicated Cloud Computing Providers for Analysis of Genomic Datasets." PMC, 2014. https://pmc.ncbi.nlm.nih.gov/articles/PMC4172764
21. "Governing synthetic biology and AI convergence: emerging biosecurity priorities for Africa." Frontiers in Bioengineering and Biotechnology, 2026. https://frontiersin.org/journals/bioengineering-and-biotechnology/articles/10.3389/fbioe.2026.1834976/full
22. "Securing Dual-Use Pathogen Data of Concern." arXiv:2602.08061. https://arxiv.org/pdf/2602.08061
23. "From capability uplift to capability governance: an AI-biosecurity stack." Frontiers in Microbiology, 2026. https://frontiersin.org/articles/10.3389/fmicb.2026.1899413/full
24. "ClawBench: Benchmarking large language models for ACMG/AMP variant interpretation." bioRxiv, 2026. https://biorxiv.org/content/10.64898/2026.06.30.735646v1.full.pdf
25. "AI coding agents hit 60x speedups but can't validate their own output." https://bizstack.tech/ai-coding-agents-hit-60x-speedups-but-cant-validate-their-own-output
26. "Agentic genomics: From pipeline automation to autonomous validation." https://eigenius.online/articles/agentic-genomics-verification
27. "Hardness of Covering Alignment: Phase Transition in Post-Sequence Genomics." arXiv:1611.05086. https://ar5iv.labs.arxiv.org/html/1611.05086
28. "Parameterized Algorithms in Bioinformatics: An Overview." Algorithms, 2019. https://doi.org/10.3390/a12120256
29. "Phase transition in the computational complexity of the shortest common superstring and genome assembly." PubMed, 2025. https://pubmed.ncbi.nlm.nih.gov/38366408
