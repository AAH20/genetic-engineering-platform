# Cluster 2: Protein Engineering Biosecurity

## Overview

Protein engineering biosecurity addresses the dual-use risks arising from AI-driven protein design, synthetic biology, and automated biofoundries. The convergence of generative AI models (ProteinMPNN, AlphaFold3, ESM3), laboratory automation, and accessible DNA synthesis has fundamentally altered the threat landscape, rendering traditional list-based screening inadequate.

---

## 1. Biosecurity Governance

### Regulatory Frameworks
- **U.S. Federal Select Agent Program (FSAP)**: Requires written security plans under 42 CFR 73.11 (HHS), 7 CFR 331.11 (USDA plant), 9 CFR 121.11 (USDA veterinary). Performance-based requirements covering risk assessment, access control, personnel suitability, inventory control, incident response, and information systems security.
- **U.S. Policy on Dual Use Research of Concern (DURC)**: Relies on static lists of specific agents and experimental manipulations; fails to capture versatile AI-biology tools.
- **Australia Biosecurity Act 2015**: Comprehensive framework with compliance and enforcement powers, human biosecurity control orders, and import risk analyses.
- **China's 2020 Biosecurity Law**: Elevates biosecurity to national security priority but remains focused on physical containment rather than algorithmic risks.
- **Biosecurity Modernization and Innovation Act of 2026 (BMIA)**: First legislative step toward consolidating U.S. biosecurity governance; requires White House to identify gaps and develop implementation plan.

### Proposed Frameworks
- **IAB Capability Framework** (5 levels): Zero-shot prediction → Advanced prediction → Targeted sequence generation → Integrated design & active learning → Full AI-Bio automation. Risk escalates from Low-Moderate to Extremely High.
- **Three-tier KYC Framework**: Tier I (institutional trust anchors), Tier II (output screening via homology/functional annotation), Tier III (behavioral monitoring).
- **Function-based Screening**: Moves beyond sequence similarity to detect hazardous biological functions regardless of similarity to known SoCs. Leverages VFDB, PHI-base, FunSoCs, PathGO annotation frameworks.
- **Relational Biosecurity**: Treats interactions between components as explicit objects of design and governance; emphasizes system-level sensing and compositional workflow oversight.

---

## 2. Bottlenecks

1. **Homology-based screening blind spot**: AI-generated proteins may be functionally equivalent to known toxins while sharing little sequence similarity, rendering current screening ineffective.
2. **Static agent lists**: DURC and select agent frameworks rely on fixed lists that cannot capture novel AI-designed threats.
3. **Decentralized DNA synthesis**: Benchtop synthesis systems and global market expansion bypass centralized screening.
4. **Expertise lowering**: AI tools and biofoundries reduce the expertise required for sophisticated protein engineering, widening access.
5. **Jurisdictional fragmentation**: "Ethics dumping" occurs when research migrates to jurisdictions with less stringent oversight.
6. **Oversight gap for non-institutional actors**: Individuals not affiliated with universities or federal labs often escape biosafety/biosecurity requirements.
7. **Function prediction limitations**: Reliable prediction of biological function from sequence remains beyond current capabilities, complicating screening.

---

## 3. Cost Tradeoffs

- **Australia's biosecurity budget**: $792M AUD (2023-24), projected to $811M AUD (2027-28), with cost recovery ($379M) and base appropriations ($366M) as primary sources.
- **Screening costs**: Function-based screening requires significant R&D investment but may reduce long-term risk exposure.
- **Compliance costs**: FSAP registration, security plans, access control systems, and personnel screening impose substantial overhead on registered entities.
- **Cost recovery models**: Australia uses import declaration charges, permit fees, and quarantine charges to fund biosecurity activities.
- **Innovation vs. security**: Layered mitigation strategies must balance open scientific progress with robust safeguards to avoid stifling innovation.

---

## 4. Failure Modes

1. **Designer toxin creation**: AI-designed proteins with enhanced lethality, stability, or novel mechanisms evade detection.
2. **Viral fitness optimization**: pLMs integrated with active learning can optimize virulence or immune escape with minimal human oversight.
3. **Automated biofoundry exploitation**: Closed-loop DBTL systems enable high-throughput exploration of dangerous sequence space.
4. **Supply chain vulnerabilities**: Decentralized DNA synthesis and benchtop systems bypass screening infrastructure.
5. **Model misuse**: LLM agents can substantially lower barriers to protein design (ABLE benchmark shows 7/15 frontier models refuse all tasks, but others perform substantially).
6. **Homology evasion**: Novel sequences with no similarity to known threats pass through screening undetected.
7. **Institutional accountability gaps**: Lack of shared responsibility between research institutions and model hosts.

---

## 5. Hardware Requirements

- **Access control systems**: Card/biometric readers, door/alarm integration with durable, exportable audit logs tied to individual credentials.
- **Inventory tracking**: LIMS platforms with chain-of-custody logging, role-based permissions, and physical count reconciliation.
- **Physical security**: Perimeter security, line of separation, rodent/wildlife control (agricultural biosecurity).
- **Computing infrastructure**: Powerful computers required to run generative AI models locally; biofoundries require robotic synthesis and testing platforms.
- **Network security**: Protection of electronic records, inventory databases, and access-control systems from unauthorized access.
- **BSEQ evaluation**: Hardware and software security lifecycle management for bioeconomy instruments.

---

## 6. Most Cited Papers

1. **"Protein design, generative AI and biological security"** (Frontiers in Microbiology, 2026) - Reviews generative protein design landscape, dual-use implications, and layered mitigation strategies.
2. **"Without safeguards, AI-Biology integration risks accelerating future pandemics"** (NCBI/PMC, 2025) - Proposes IAB capability framework with five escalating risk levels.
3. **"Beyond sequence similarity: toward function-based screening of nucleic acid synthesis"** (Frontiers in Bioengineering, 2026) - Advocates function-based screening to detect hazardous functions regardless of sequence similarity.
4. **"Know your scientist: KYC as biosecurity infrastructure"** (Frontiers in Microbiology, 2026) - Proposes three-tier KYC framework inspired by AML practices.
5. **"Agentic BAIM-LLM Evaluation (ABLE)"** (arXiv, 2026) - Benchmarks 15 frontier LLMs on dual-use protein design workflows.
6. **"Protein engineering: security implications"** (PMC, 2005) - Early assessment of protein toxin manipulation risks and calls for regulation.
7. **"Addressing Biosecurity Concerns Related to Synthetic Biology"** (NSABB, 2007) - Foundational report on synthetic biology oversight.
8. **"Toward relational biosecurity"** (Frontiers in Microbiology, 2026) - System-level approach to AI-enabled biology governance.
9. **"Transforming American Biosecurity"** (FAS, 2026) - Diagnostic case for institutional reform with seven design requirements.
10. **"Proteo-R1: Reasoning Foundation Models for De Novo Protein Design"** (arXiv, 2026) - Dual-expert architecture decoupling molecular understanding from geometric generation.

---

## 7. NP-Hard Problems

1. **Function prediction from sequence**: Reliably predicting biological function from protein sequence remains computationally intractable for novel designs.
2. **Sequence space exploration**: The vastness of protein sequence space (>>10^77 for 75-residue proteins) makes exhaustive screening impossible.
3. **Homology detection**: Detecting functional similarity without sequence similarity requires solving inverse folding and binding prediction problems.
4. **Multi-objective optimization**: Simultaneously optimizing for stability, binding affinity, and function while avoiding hazardous properties.
5. **Active learning efficiency**: Identifying functional mutations from minimal data in high-dimensional sequence spaces.
6. **Compositional workflow oversight**: Representing and propagating system-level objectives across distributed AI-bio components.

---

## 8. OSS Projects

1. **ProteinMPNN** (Dauparas et al., 2022): Sequence recovery tool for protein design; used in ABLE benchmark.
2. **AlphaFold3** (Abramson et al., 2024): Structure prediction tool; integrated into dual-use workflows.
3. **RFdiffusion** (Watson et al., 2023): Generative model for protein design.
4. **ESM-IF1** (Hsu et al., 2022): Inverse folding model for generative enzyme/antibody design.
5. **EVEscape** (Thadani et al., 2023): Predicts viral escape variants.
6. **VIRAL** (Huot et al., 2025): Predicts viral evolution.
7. **ProteinNPT** (Notin et al., 2023): Active learning framework for protein engineering.
8. **EVOLVEpro** (Jiang et al., 2024): Direct evolution framework.
9. **iBioFAB** (Yu et al., 2023): Automated biofoundry platform.
10. **Fun GCAT** (IARPA): Functional Genomic and Computational Assessment of Threats program.

---

## 9. Scalability Limits

1. **Screening throughput**: Current homology-based screening cannot scale to match the output of AI design tools and biofoundries.
2. **Regulatory lag**: Governance frameworks cannot keep pace with rapid technological advancement.
3. **Global coordination**: Lack of international harmonization creates enforcement gaps and ethics dumping.
4. **Computational resources**: Function-based screening requires significant computational infrastructure for biophysical modeling.
5. **Data availability**: Training effective screening models requires comprehensive functional annotation data.
6. **Institutional capacity**: Smaller institutions lack resources to implement robust biosecurity programs.
7. **Decentralized synthesis**: Benchtop DNA synthesis systems scale beyond centralized oversight.

---

## 10. SOTA Approaches

1. **Function-based screening**: Detects hazardous biological functions using biophysical and biochemical constraints rather than sequence similarity.
2. **Layered mitigation**: Combines sequence screening, nucleic acid screening, and software-level security measures.
3. **Capability-oriented risk assessment**: Evaluates AI-biology systems based on integration depth (IAB framework).
4. **KYC-inspired verification**: Institutional vetting, output screening, and behavioral monitoring.
5. **Relational biosecurity**: System-level governance of compositional workflows.
6. **Test-before-deployment**: Formal testing mechanisms for new governing instruments (BMIA requirement).
7. **Responsible AI x Biodesign**: Community initiative for responsible development of AI technologies in protein design.
8. **BIO-ISAC BSEQ**: Biosecurity Evaluation Questionnaire for hardware/software lifecycle security.

---

## Key Citations

- Frontiers in Microbiology (2026): "Protein design, generative AI and biological security"
- NCBI/PMC (2025): "Without safeguards, AI-Biology integration risks accelerating future pandemics"
- Frontiers in Bioengineering (2026): "Beyond sequence similarity: toward function-based screening"
- Frontiers in Microbiology (2026): "Know your scientist: KYC as biosecurity infrastructure"
- arXiv (2026): "ABLE: Benchmarking LLM Use of Protein Design Tools"
- NSABB (2007): "Addressing Biosecurity Concerns Related to Synthetic Biology"
- FAS (2026): "Transforming American Biosecurity"
- Frontiers in Microbiology (2026): "Toward relational biosecurity"
- Springer (2025): "Protein engineering as a driver of innovation in therapeutics"
- PMC (2005): "Protein engineering: security implications"
