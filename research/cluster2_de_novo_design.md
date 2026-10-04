# Cluster 2: De Novo Protein Design — Research Synthesis

**Date:** 2026-10-04
**Method:** 10 parallel web searches, top 3 results each, synthesized with bottlenecks and citations.

---

## 1. De Novo Protein Design Review

De novo protein design creates entirely new protein structures and functions from physical principles and computational methods, rather than modifying natural proteins. The field was recognized with the **2024 Nobel Prize in Chemistry** awarded to David Baker.

**Standard workflow (3 steps):**
1. **Backbone construction** — Hallucination, RFdiffusion, RFdiffusion All-atom
2. **Sequence optimization** — Rosetta, ProteinMPNN, LigandMPNN
3. **Candidate evaluation** — Rosetta scores (ddG, SASA), AF2 metrics (pLDDT, RMSD, PAE, pTM)

**Key breakthrough:** Deep learning (AlphaFold2 2021, ProteinMPNN 2022, RFdiffusion 2023) has systematically reshaped the field. Experimental validation of <100 sequences can now identify high-affinity binders (e.g., Glögl et al. tested 96 sequences, found sub-10 pM TNFR1 binder).

**Citations:**
- De novo protein design: a transformative frontier in clinical protein applications. *J Transl Med* (2026). PMC12958671
- The past, present and future of de novo protein design. *Nature* (2026). bakerlab.org
- Code to complex: AI-driven de novo binder design. *Structure* (2025). Cell Press

---

## 2. Protein Design Is NP-Hard

The protein design problem — finding the minimum-energy amino acid sequence for a target structure — is **provably NP-hard** (Pierce & Winfree, 2002, cited 366+). Even the pairwise discrete model with fixed backbone is NP-hard to approximate.

**Practical workarounds:**
- **Sparse Residue Interaction Graphs (SPRIG):** Delete edges with small interaction energies → polynomial-time solvable for many real cases
- **Weighted Constraint Satisfaction (WCSP):** Cost function networks with provable guarantees
- **Quantum computing:** Grover's algorithm circuits explored for small instances (PMC10124842)
- **Heuristic methods:** Metropolis Monte Carlo / simulated annealing (Rosetta) — fast but no optimality guarantee

**Implication:** All practical protein design relies on heuristics or approximations; exact solutions are intractable for biologically relevant sizes.

**Citations:**
- Protein Design is NP-hard. *Pierce NA, Winfree E.* PEDS (2002). Cited 366+
- Protein Design by Provable Algorithms. *PMC6788629*
- Gate-based quantum computing for protein design. *PMC10124842*

---

## 3. RFdiffusion

**RFdiffusion** (Watson et al., Nature 2023) is the state-of-the-art diffusion-based generative model for de novo protein backbone generation. It fine-tunes RoseTTAFold on structure denoising tasks.

**Key properties:**
- SE(3)-equivariant (rigid-frame representation: Cα coordinate + N-Cα-C orientation)
- 200-step denoising diffusion process
- Conditioning on functional motifs, distance/orientation constraints, 3D coordinates

**Validated applications:**
- Unconditional & topology-constrained monomer design
- Protein binder design (cryo-EM structure of influenza HA binder nearly identical to model)
- Symmetric oligomer design
- Enzyme active site scaffolding
- Metal-binding protein design

**Follow-on:** RFdiffusion All-atom (RFD3, Butcher et al. 2025) — all-atom generation inspired by AlphaFold3 architecture.

**Citations:**
- De novo design of protein structure and function with RFdiffusion. *Watson R et al., Nature* (2023). doi:10.1038/s41586-023-06415-8
- RFDiffusion: SE(3)-Equivariant Protein Design. *Emergent Mind* (2026)
- Design-CP: Context Parallelism for Design of Protein Nanoparticles. *arXiv:2607.05439* (2026)

---

## 4. Protein Design Algorithms

**Three methodological paradigms** (MDPI 2026 review):

| Paradigm | Description | Examples |
|---|---|---|
| **Sequence–structure decoupled** | Generate backbone → design sequence | Hallucination, RFdiffusion + ProteinMPNN |
| **Hybrid** | Two-stage with predictor-driven iterative co-refinement | AF2-guided design cycles |
| **Co-design** | Joint generative sequence+structure | Explicit joint formulations |

**Physics-based era:** Rosetta (energy minimization), molecular dynamics, fragment assembly
**Deep learning era:** ProteinMPNN (graph neural network for sequence design), RFdiffusion (diffusion for backbone), ProGen (autoregressive language model), ESM-2/ESM-Fold

**Evaluation metrics:** Physical validity, folding consistency, design coverage, pLDDT, RMSD, PAE, TM-score

**Citations:**
- Generative Protein Design: From Deep Learning Algorithms to Translational Applications. *MDPI IJMS* (2026). 1422-0067/27/9/3917
- Computational protein design. *Nature Reviews Bioengineering* (2025). s43586-025-00383-1
- Protein design and RNA design: Perspectives. *PMC12798782*

---

## 5. De Novo Enzyme Design

**Rosetta protocol (4 stages):**
1. Choose catalytic mechanism + minimal active site model
2. Identify scaffold sites compatible with active site
3. Design active site geometry + catalytic residues
4. Sequence design + experimental screening

**Historical limitations:**
- Early designs had very low catalytic efficiencies (kcat/KM ~10²–10³ M⁻¹s⁻¹ vs. natural enzymes ~10⁶–10⁸)
- Active site preorganization insufficient (crystal structures showed deviations from design models)
- Limited to simple reactions (retro-aldol, Kemp elimination, Diels-Alder)

**Recent progress:**
- ML-generated enzymes with efficiencies approaching natural enzymes
- ProGen fine-tuned on enzyme families → variants with ~31% sequence identity to training set
- Challenges remain: high-energy barriers, multistep mechanisms, conformational dynamics

**Citations:**
- De Novo Enzyme Design Using Rosetta3. *Richter F et al., PMC3095599* (2011)
- De novo enzyme design: Controlling structure to design function. *Listov D et al., PubMed 41849863*
- Structural analyses of covalent enzyme-substrate analogue complexes. *Wang L et al., PMC3440004*

---

## 6. Open-Source Software Tools

| Tool | Type | Key Features |
|---|---|---|
| **Rosetta** | Physics-based suite | Energy minimization, docking, design; industry standard |
| **ProteinMPNN** | DL sequence design | Graph neural network; fast, high recovery rates |
| **RFdiffusion** | DL backbone generation | Diffusion model; conditional design |
| **OSPREY 3.0** | Provable design | GPU-accelerated, 100× faster than v2, Python API |
| **ColabDesign** | Hallucination | JAX-based, binder design |
| **Ovo** | Ecosystem | Nextflow orchestration, data management, visualization |
| **ProteinDJ** | HPC pipeline | Nextflow + Apptainer for HPC deployment |
| **protein-design-mcp** | MCP server | 19 tools: RFdiffusion, ProteinMPNN, ESMFold, AF2, Boltz, PyRosetta |
| **OpenProtein.AI** | Platform | No-code, PoET language model, free for academia |

**Citations:**
- OSPREY 3.0. *J Comput Chem* (2018). PMID 30368845
- Ovo, an open-source ecosystem for de novo protein design. *Commun Biol* (2026). PMID 42321544
- ProteinDJ: A high-performance and modular protein design pipeline. *PMC12820799*

---

## 7. Hardware Requirements

| Model | VRAM (FP16) | VRAM (Q8) | VRAM (Q4) |
|---|---|---|---|
| RFdiffusion (200M params) | 16 GB | 10 GB | 8 GB |
| AlphaFold2 (93M params) | 16 GB | 12 GB | 8 GB |

**Recommendations:**
- **Minimum:** 8 GB VRAM
- **Recommended:** 12–24 GB (RTX 4090, L40, A100)
- **Ideal:** 80 GB (H100) — ~4× faster than A100
- **Large assemblies:** Multi-GPU required (Design-CP: 2D grid sharding with ring attention)

**Throughput matters more than VRAM:** 100–1000 candidates per campaign typical. H100 generates 900-residue trajectory in 2–3 hours; 250 residues in ~5 minutes.

**Citations:**
- Best GPU for Protein Design — RFdiffusion & De Novo Design (2026). vramfirst.com
- One-shot design of functional protein binders with BindCraft. *Nature* (2025). s41586-025-09429-6
- Design-CP: Context Parallelism for Design of Protein Nanoparticles. *arXiv:2607.05439*

---

## 8. Cost Analysis

**Traditional drug discovery:**
- Lead optimization: **$5M–$15M per candidate**, 12–36 months
- Only 1 in 14.6 candidates reaches market

**AI-driven campaigns (Anthropic 2026):**
- 120 GPU-hours per binder (H100)
- 12,500 H100-hours per multi-target session
- 354 confirmed binders from 1,320 designs (26.7% hit rate)
- 40% hit rate on RBX1 vs. 3.7% for 245 human entrants

**Gene synthesis costs:**
- Tens to hundreds of dollars per gene
- Variational Synthesis (JURA Bio): 10¹⁷ unique sequences in single reaction

**CRADLE-1:** 4–7× faster than rational design in lead optimization

**Citations:**
- Claude Ran a Protein Design Campaign Alone. *TensorFeed* (2026)
- Coevolution-informed Bayesian optimization for sample-efficient protein design. *bioRxiv* (2026)
- What comes after de novo? Automated lead optimization with CRADLE-1. *bioRxiv* (2026)

---

## 9. Scalability Limits

**Sequence space explosion:** 20^N possible sequences for N residues. Functional proteins occupy an astronomically small subset.

**Current bottlenecks:**
- Low in silico success rates → thousands of designs needed
- GPU-hundreds of hours per campaign
- Tool fragmentation: hard to install, deploy, integrate
- Large assemblies exceed single-GPU memory (quadratic scaling in residues)

**Solutions in progress:**
- **RSO (Relaxed Sequence Optimization):** Designs up to 1000 aa without retraining; 100+ proteins experimentally validated
- **ProteinDJ:** HPC deployment via Nextflow
- **Design-CP:** Multi-GPU context parallelism for large nanoparticles
- **Variational Synthesis:** 10¹⁷ sequences per synthesis run

**Citations:**
- Scalable protein design using optimization in a relaxed sequence space. *Frank C et al., Science* (2024). 386(6720):439-445
- ProteinDJ. *PMC12820799*
- Design-CP. *arXiv:2607.05439*

---

## 10. Biosecurity & Governance

**Key concern:** De novo proteins are not homologous to natural proteins → existing DNA synthesis screening (homology-based) is **outdated**.

**Baker & Church proposal (Science, Jan 2024):**
- All synthetic gene sequences should be collected and stored in encrypted repositories
- Queried only in emergencies
- Screening integrated with synthesis process itself

**Three intervention levels:**
1. **Sequence screening** — check designed protein sequences
2. **Nucleic acid screening** — check DNA before production
3. **Software safeguards** — controlled access, logging, built-in biosecurity

**Additional measures:**
- Targeted unlearning of harmful knowledge from models
- Export control on design tools
- Legal requirements for screening genome synthesis orders

**Citations:**
- Protein design meets biosecurity. *Baker D, Church G., Science* (2024). 383(6681):349. doi:10.1126/science.ado1671
- Security challenges by AI-assisted protein design. *Hunter P., EMBO Rep* (2024). PMID 38532127
- Protein design, generative AI and biological security. *Front Microbiol* (2026). 10.3389/fmicb.2026.1817535

---

## Summary of Bottlenecks

1. **NP-hard optimization** — no exact solutions; all methods are heuristics
2. **Low success rates** — thousands of designs needed per hit
3. **GPU compute cost** — 100–12,500 H100-hours per campaign
4. **Tool fragmentation** — hard to install, deploy, integrate
5. **Scalability ceiling** — single-GPU memory limits for large assemblies
6. **Enzyme design gap** — catalytic efficiencies far below natural enzymes
7. **Biosecurity lag** — screening infrastructure not ready for de novo sequences
8. **Clinical translation** — ~90% phase I failure rate; manufacturing consistency unproven
