# Cluster 2: Protein Engineering OSS Tools — Research Synthesis

**Date:** 2026-10-04
**Search queries:** 10 (protein engineering OSS tools, PyMOL, RDKit protein, Open Babel, Biopython protein, protein tools hardware requirements, protein tools cost analysis, protein tools scalability, protein tools biosecurity, protein tools integration)
**Results extracted:** 3 per search (30 total)

---

## 1. OSS Projects

| Project | Description | License | Key Features |
|---------|-------------|---------|--------------|
| **PyMOL** | Molecular visualization system (v3.1, Schrödinger) | Open-source foundation (source available) | 30+ file formats, 20 representations, cross-platform, Python 3.10 bundled |
| **RDKit** | Cheminformatics toolkit | BSD (GUI: GPL) | SMILES/SMARTS, substructure search, fingerprints, 2D→3D conversion, PyMOL integration, KNIME nodes |
| **Open Babel** | Chemical file format interconversion | GPL v2+ | 110+ formats, SMARTS filtering, conformer generation, force fields (MMFF94, UFF), Python/C++/Java/Perl bindings |
| **Biopython** | Python tools for computational molecular biology | Biopython license (permissive) | Sequence analysis, ProtParam (MW, pI, GRAVY, instability index), BLAST integration, v1.88 (2026) |
| **osprey 3.0** | Open-source protein redesign | Free/open-source | Python interface, protein design, mutational landscape exploration |
| **InFinity 1.0** | iGEM protein engineering framework | Open source | Modular, CSV-based input, integrates AlphaFold 2.0, ROSIE/Rosetta |
| **OpenProtein.AI / PoET** | AI-driven protein design platform | Open-source models | PoET protein language model, PoET-2 (outperforms larger models with fewer resources), no-code + API |
| **ProteinTools** (Uni Bayreuth) | Protein structure analysis toolkit | Free/open | Hydrophobic clusters, H-bond networks, salt bridges, contact maps |
| **CloudProteoAnalyzer** | Cloud-based proteomics processing | Open | HPC-distributed database searching, SaaS model, near-linear speedup to 240 CPU cores |
| **MSAID Platform** | Cloud-native proteomics platform | Commercial (open access) | Kubernetes microservices, AWS EC2, data lake, CLI/API |

---

## 2. SOTA Approaches

1. **AI-driven protein design** — OpenProtein.AI's PoET-2 outperforms much larger models using a fraction of computing resources and experimental data (MIT News, 2026)
2. **Protein language models for zero-shot prediction** — ESM-1v, ESM-C for fitness prediction, variant classification (F1 >97% for known target variants)
3. **Cloud-native proteomics** — CloudProteoAnalyzer demonstrates near-linear speedup to 12 nodes/240 cores; MSAID uses Kubernetes microservices on AWS
4. **Modular open-source frameworks** — InFinity 1.0 integrates AlphaFold 2.0 + Rosetta via CSV input for non-specialists
5. **Input screening for biosecurity** — ESM-C embedding-based screening of protein design targets (14,541 concerning human proteoforms)
6. **Protein watermarking** — SynthIDBio (Google DeepMind) embeds undetectable watermarks in AI-designed proteins via ProteinMPNN

---

## 3. Bottlenecks

- **Sequence-similarity screening is insufficient** — BLAST-based methods cannot detect AI-designed proteins with novel sequences but similar function (bioRxiv, 2026)
- **Proteogenomic scalability** — State-of-the-art tools take >0.5 months to process 1M spectra against a 3GB genome; most tools only tested on small datasets (NSF survey)
- **Database indexing with PTMs** — Space complexity of fragment-ion indexing with multiple PTMs is a fundamental scalability barrier
- **Toolchain complexity** — Intricate toolchain from raw data to results challenges biologists in installation and operation (CloudProteoAnalyzer paper)
- **Local compute limitations** — Substantial storage/resource challenges quickly exceed local compute clusters; batch-processing cloud models struggle with transfer times
- **Single-core execution** — Many proteogenomic tools (GenoSuite, Enosi, Bacterial Proteogenomic Pipeline, MSProGene) only use single execution core
- **No quantitative frameworks** — No known quantitative frameworks for scalability or quality assessment in proteogenomics

---

## 4. NP-Hard Problems

- **Protein structure prediction** — Ab initio protein folding remains computationally intractable for large proteins (addressed heuristically by AlphaFold)
- **Conformational analysis** — Low-budget conformational analysis is NP-hard; distance geometry used as approximation
- **Database searching at scale** — Searching experimental MS spectra against six-frame translated genome databases is exponential in database size
- **Protein design optimization** — Side-chain packing (rotamer optimization) is NP-hard; addressed by osprey 3.0 with heuristic methods
- **Fragment-ion indexing with PTMs** — Space complexity makes exact indexing intractable for multiple PTMs

---

## 5. Hardware Requirements

| Tool/Category | Minimum GPU | Recommended GPU | VRAM | Notes |
|---------------|-------------|-----------------|------|-------|
| ProteinMPNN | T4 | T4 | 16GB | Modal ~$0.50/hr |
| ESM | A10G | A10G | 24GB | Modal ~$1.10/hr |
| RFdiffusion | A10G | A10G | 24GB | Modal ~$1.10/hr |
| Chai | A10G | A100 | 24-40GB | Modal ~$1.10-3.50/hr |
| BoltzGen | L40S | A100 | 48-80GB | Modal ~$1.80-3.50/hr |
| AlphaFold | A100 | A100 | 40GB | Modal ~$3.50/hr |
| Proteome Discoverer 3.1 | CPU only | 2× Xeon 8-12 core | 64GB RAM | 1TB SSD, AVX2 |
| CloudProteoAnalyzer | HPC cluster | 12+ nodes, 240 cores | — | Supercomputer-scale |

**General requirements:** NVIDIA GPU with CUDA 11.7+, Python 3.10+, 16-48GB VRAM (tool-dependent)

---

## 6. Cost Tradeoffs

| Approach | Cost Model | Pros | Cons |
|----------|-----------|------|------|
| **Modal (serverless GPU)** | Pay-per-use ($0.50-3.50/hr) | No hardware ownership, 5-min setup | Ongoing cost, first-run weight downloads |
| **Local GPU** | Hardware ownership ($3K-10K+) | Full control, large campaigns | 30+ min setup, maintenance, power |
| **Cloud HPC (CloudProteoAnalyzer)** | SaaS subscription | Near-linear scalability, no local infrastructure | Subscription cost, data transfer |
| **Commercial proteomics (MSAID)** | Platform fee | Kubernetes-scaled, data lake, CLI/API | Vendor lock-in, ongoing fees |
| **Open-source (Biopython, RDKit, Open Babel)** | Free | No licensing cost, community support | Self-maintained, no formal support |
| **PyMOL** | Free (open-source) / Paid license | Open-source foundation, cross-platform | Commercial features require license |

---

## 7. Scalability Limits

- **Proteogenomic tools:** Most tested only on small datasets; no qualitative assessment on popular benchmark datasets
- **Database size:** Tools can take >0.5 months for 1M spectra against 3GB genome
- **Multi-core support:** Only a few tools (Peppy, PGMiner, PGA) support multi-core; many are single-core
- **Cloud scaling:** CloudProteoAnalyzer achieves near-linear speedup to 12 nodes/240 cores
- **PTM indexing:** Space complexity of fragment-ion indexing with multiple PTMs is a hard limit
- **Data transfer:** Batch-processing cloud models struggle with prolonged transfer times and lack of integrated storage
- **Local clusters:** Not easily scalable; substantial storage/resource challenges quickly exceed capacity

---

## 8. Failure Modes

- **Sequence-similarity screening failure** — AI-designed proteins with low sequence similarity to natural proteins evade BLAST-based detection
- **CUDA out of memory** — Common with large proteins or high design counts; mitigated by reducing --num-designs or using larger GPUs
- **Watermark dilution** — Fusing AI-designed proteins with natural proteins (e.g., fluorescent tags) can dilute SynthIDBio watermarks
- **Short protein watermarking** — Very short proteins may incorporate too few watermark amino acids for identification
- **Key distribution vulnerability** — SynthIDBio security depends entirely on key distribution/maintenance infrastructure
- **Tool integration failure** — ROSIE platform developed by different groups over time makes seamless module integration difficult
- **False positive flagging** — 23% of human proteins and 63% of antibody patent targets flagged as dual-use, potentially burdening legitimate research

---

## 9. Biosecurity Governance

- **Input screening framework** — First screening framework for protein design tools; screens targets (not outputs) using ESM-C embeddings against 14,541 concerning human proteoforms
- **IAB capability levels** — Five-level framework: (1) Zero-shot prediction, (2) Advanced prediction, (3) Targeted sequence generation, (4) Integrated design & active learning, (5) Full AI-Bio automation
- **Protein watermarking** — SynthIDBio enables DNA synthesizers to identify AI-designed proteins from trusted sources
- **DURC limitations** — US DURC policy relies on static agent lists, fails to capture versatile pLM dual-use potential
- **DNA synthesis screening gap** — Existing screening operates at digital-physical interface; no tools existed to screen user requests to protein design tools (prior to 2026 framework)
- **Tiered trusted access** — Proposed to address overlap between targets of concern and therapeutic targets

---

## 10. Most Cited Papers

1. **osprey 3.0: Open-Source Protein Redesign for You** — Hallen et al., 2018, cited by ~95 (PMC6391056)
2. **Biopython: freely available Python tools for computational molecular biology and bioinformatics** — Cock et al., 2009, Bioinformatics 25(11):1422-3
3. **ProteinTools: a toolkit to analyze protein structures** — Ferruz, Schmidt, Höcker, 2021, Nucleic Acids Research, gkab375
4. **CloudProteoAnalyzer: scalable processing of big data from proteomics using cloud computing** — Li et al., 2024, PMC10942798
5. **Safety first: input screening for protein design tools** — bioRxiv, 2026 (10.64898/2026.08.04.740855)
6. **Without safeguards, AI-Biology integration risks accelerating future pandemics** — PMC12872745
7. **RDKit: Open-source cheminformatics** — Landrum (recommended citation, DOI: 10.5281/zenodo.591637)
8. **Open Babel: interconversion of chemical file formats** — O'Boyle et al., J. Cheminf. (2019) v11, article 49

---

## 11. Citations

1. MIT News (2026). "Bringing AI-driven protein-design tools to biologists everywhere." https://news.mit.edu/2026/bringing-ai-driven-protein-design-tools-everywhere-0417
2. Hallen, M.A. et al. (2018). "osprey 3.0: Open-Source Protein Redesign for You." PMC6391056.
3. iGEM Team Sporadicate (2022). "Protein engineering in the computational age: An open source framework." PMC10715127.
4. PyMOL (2026). https://www.pymol.org/
5. RDKit (2026). https://www.rdkit.org / https://github.com/rdkit/rdkit
6. Open Babel (2026). https://openbabel.org / https://github.com/openbabel/openbabel
7. Biopython (2026). https://biopython.org/ v1.88
8. adaptyvbio/protein-design-skills. "Compute Setup." https://github.com/adaptyvbio/protein-design-skills/blob/main/docs/compute-setup.md
9. Thermo Fisher Scientific. "Proteome Discoverer 3.1 User Guide — System Requirements."
10. Li, J. et al. (2024). "CloudProteoAnalyzer: scalable processing of big data from proteomics using cloud computing." PMC10942798.
11. NSF PAR (2024). "Methods for Proteogenomics Data Analysis, Challenges, and Scalability Bottlenecks: A Survey." par.nsf.gov/servlets/purl/10221848
12. Schneider, M. et al. (2025). "A Scalable, Web-Based Platform for Proteomics Data Processing." J. Proteome Research, 10.1021/acs.jproteome.4c00871
13. bioRxiv (2026). "Safety first: input screening for protein design tools." 10.64898/2026.08.04.740855
14. Ars Technica (2026). "Google figures out how to watermark AI-designed proteins."
15. PMC12872745. "Without safeguards, AI-Biology integration risks accelerating future pandemics."
16. Ferruz, N. et al. (2021). "ProteinTools: a toolkit to analyze protein structures." Nucleic Acids Research, gkab375. https://www.proteintools.uni-bayreuth.de/
