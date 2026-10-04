# Cluster 5: Computational Genomics Biosecurity

## Overview

Computational genomics biosecurity addresses the dual-use risks arising from the convergence of AI-driven biological design, DNA synthesis, and genomic data sharing. The field spans technical safeguards (sequence screening, adversarial robustness), governance frameworks (IGSC, NIH GDS, WHO principles), and infrastructure requirements (access control, audit systems).

---

## 1. Biosecurity Governance

### Key Frameworks

| Framework | Scope | Key Mechanism |
|-----------|-------|---------------|
| **International Gene Synthesis Consortium (IGSC)** | Commercial DNA synthesis providers | Voluntary sequence screening + customer verification |
| **NIH Genomic Data Sharing (GDS) Policy** | Federally funded genomics research | Controlled access via Data Access Committees (dbGaP) |
| **WHO Genomic Data Principles** | Global human genomic data | Ethical collection, access, use, and sharing guidelines |
| **Federal Select Agent Program (FSAP)** | US select agents/toxins | Mandatory security plans (42 CFR 73, 7 CFR 331, 9 CFR 121) |
| **Biosecurity Act 2015 (Australia)** | National biosecurity | Import risk analysis, compliance enforcement |
| **BIO-ISAC BSEQ** | Bioeconomy hardware/software | Security evaluation questionnaire for equipment procurement |

### Governance Gaps Identified

- **Sequence-centered governance limitations**: Current screening relies on sequence identity to known threats, vulnerable to codon optimization and AI-designed synthetic homologs (Wittmann et al., 2025)
- **Voluntary vs. mandatory standards**: IGSC screening is voluntary; companies outside participating networks are not bound
- **International coordination**: Biological Weapons Convention lacks operational rules for gene synthesis screening
- **AI-era governance**: Existing frameworks designed for known pathogens, not AI-generated novel sequences

---

## 2. Bottlenecks

### Technical Bottlenecks

1. **Sequence-based screening evasion**: AI-assisted protein design can produce synthetic homologs with minimal sequence identity to known threats, evading BSS tools (Wittmann et al., 2025)
2. **Adversarial genomic sequences**: Genomic foundation models (DNABERT-2, Nucleotide Transformer v2) vulnerable to perturbation-efficient attacks requiring only a few nucleotide edits (TAIS 2026)
3. **Context length limitations**: Standard transformers face quadratic scaling; long genomic contexts require sub-quadratic architectures (Hyena DNA)
4. **Fragment detection**: BSS tools struggle to detect short fragments (50 nt) of synthetic homologs
5. **Reference database coverage**: Screening effectiveness depends on curated pathogen databases; novel variants evade detection

### Operational Bottlenecks

6. **DBTL cycle**: Design-Build-Test-Learn cycle remains a bottleneck; experimental validation lags computational design
7. **Data sharing vs. privacy tension**: Broad sharing needed for research, but re-identification risks persist
8. **Consent management**: Differing subject consents across studies complicate data aggregation
9. **Decentralized synthesis**: Benchtop synthesis devices bypass centralized screening

---

## 3. Most Cited Papers

1. **Wittmann et al. (2025)** - "The limits of sequence-based biosecurity screening tools in the age of AI-assisted protein design" - Demonstrated AIPD tools evading BSS via synthetic homologs
2. **NIST IR 8432 (2023)** - "Cybersecurity of Genomic Data" - Comprehensive framework for genomic data cybersecurity
3. **Zhou et al. (2024)** - DNABERT-2 - Genomic foundation model for sequence understanding
4. **Dalla-Torre et al. (2024)** - Nucleotide Transformer v2 - Scalable genomic foundation model
5. **Brixi et al. (2026)** - Evo 2 - Long-context biological language model with open-source release
6. **National Academies (2025)** - "The Age of AI in the Life Sciences" - AI capability uplift assessment
7. **Pannu (2026)** - "Shaping AI progress for biology and biosecurity" - Three-part series on AIxBio policy
8. **Feldman et al. (2026)** - "Know your scientist: KYC as biosecurity infrastructure" - Three-tier KYC framework

---

## 4. SOTA Approaches

### Defensive Technologies

| Approach | Description | Status |
|----------|-------------|--------|
| **Dual-mandate paradigm** | Generation models inverted for detection/discrimination | Radical Numerics (Evo/Omni) |
| **Sub-quadratic architectures** | Hyena convolutions for 1M+ bp context | Hyena DNA |
| **Protein watermarking** | SynthID-style watermarks in AI-designed proteins | Google DeepMind |
| **KYC framework** | Three-tier: institutional vetting + output screening + behavioral monitoring | Proposed (Feldman et al.) |
| **Adversarial training** | Iterative hardening of GFMs against perturbations | Reduces attack success from 40-45% to 20-30% |
| **Structure-informed screening** | 3D protein structure comparison for functional similarity | Research stage |
| **Embedding-based screening** | ML-learned sequence representations for non-obvious relationships | Emerging |

### Screening Approaches Comparison

| Method | Strength | Limitation |
|--------|----------|------------|
| Nucleotide-level alignment | Sensitive for known sequences | Weakened by codon optimization |
| Protein-level alignment | Detects functional similarity | Database coverage dependent |
| Profile-based screening | Remote functional relationships | Requires expert curation |
| Structure-informed | Sequence divergence robust | Computationally demanding |
| ML-assisted | Non-obvious relationships | Validation/interpretability needed |

---

## 5. Failure Modes

1. **Adversarial evasion**: Small nucleotide edits (transversions favored) in 5' regulatory regions evade GFM-based screening
2. **Synthetic homolog generation**: AI-designed proteins with minimal sequence identity but retained function
3. **Re-identification**: Genomic data re-identified using genealogical databases and public records
4. **Consent violations**: Data used beyond original consent scope
5. **Fragmentation attacks**: Hazardous sequences split into undetectable fragments
6. **Open-weight model misuse**: Safety-aligned models stripped of guardrails
7. **Decentralized synthesis bypass**: Benchtop devices circumvent provider screening
8. **Context rot**: Standard transformers lose signal fidelity over long sequences

---

## 6. Hardware Requirements

### Laboratory Infrastructure

- **Access control systems**: Card/biometric readers, door/alarm integration
- **Inventory tracking**: LIMS platforms with chain-of-custody logging
- **Audit systems**: Durable, exportable logs tied to individual credentials
- **Physical security**: Perimeter security, line of separation, rodent/wildlife control

### Computational Infrastructure

- **GPU clusters**: Large-scale genomic model training (Evo: 7B parameters)
- **High-throughput sequencing**: Environmental surveillance, metagenomic analysis
- **Secure data storage**: Encrypted genomic databases with access controls

### Biosecurity-Specific Hardware

- **Biosafety cabinets**: BSL-2/3/4 containment
- **Autoclaves**: Sterilization equipment
- **Environmental sensors**: Pathogen detection systems

---

## 7. Cost Tradeoffs

### Biosecurity Investment (Australia FY 2023-24)

| Category | Cost (AUD) |
|----------|------------|
| Cost recovery | $379.1M |
| Base appropriation | $366.4M |
| STEPS program | $46.5M |
| **Total** | **$792.0M** |

### Cost-Benefit Considerations

- **Screening costs**: Sequence screening adds overhead to synthesis orders
- **Compliance costs**: BCAP audits require documentation, training, virtual/in-person reviews
- **Data storage**: GDC maintains >2 petabytes of cancer genomic data
- **R&D investment**: AI safety research vs. capability development tradeoff

### Cost Recovery Mechanisms

- Import declaration charges ($46-71 AUD)
- Permit application fees ($130-135 AUD)
- Animal quarantine charges ($269-4,447 AUD)
- Approved arrangement fees ($285-2,966 AUD)

---

## 8. Scalability Limits

### Computational Scaling

- **Transformer quadratic scaling**: Self-attention limits context to ~10K tokens without optimization
- **Sub-quadratic solutions**: Hyena convolutions enable 1M+ bp context
- **Model size**: Evo 7B parameters; Evo 2 extends to long genomic contexts

### Synthesis Scaling

- **Oligonucleotide length**: Increased from ~300 bases (2015) to >1,000 bases (2026)
- **Parallel synthesis**: Chip-based approaches enable massive parallelism
- **Decentralization**: Benchtop systems increase access but complicate screening

### Data Scaling

- **Genomic data growth**: Exponential increase in sequencing data
- **Storage requirements**: Petabyte-scale repositories (GDC, TCGA)
- **Processing demands**: Real-time screening of synthesis orders

---

## 9. NP-Hard Problems

1. **Sequence alignment**: Optimal alignment of long genomic sequences is computationally intensive
2. **Protein structure prediction**: Ab initio prediction remains challenging (AlphaFold addresses partially)
3. **Metagenomic assembly**: Reconstructing genomes from mixed environmental samples
4. **Regulatory element identification**: Distinguishing functional non-coding elements
5. **Pathogenicity prediction**: Predicting variant effects across diverse genetic backgrounds
6. **Adversarial robustness**: Certifying model robustness against bounded perturbations

---

## 10. OSS Projects

| Project | Description | License |
|---------|-------------|---------|
| **Evo / Evo 2** | Generative genomic foundation model (7B params) | Open source (Brixi et al., 2026) |
| **DNABERT-2** | Genomic sequence understanding model | Open source (Zhou et al., 2024) |
| **Nucleotide Transformer v2** | Scalable genomic foundation model | Open source (Dalla-Torre et al., 2024) |
| **OpenGenome2** | Genomic training dataset | Open source |
| **BSS tools** | Biosecurity screening software (various providers) | Proprietary/Open |
| **BSEQ** | Biosecurity Evaluation Questionnaire | Open (BIO-ISAC) |

---

## 11. Compliance Requirements

### US Federal

- **FSAP registration**: Mandatory security plans for select agent possession
- **NIH GDS Policy**: Data sharing plans required for funding
- **Common Rule**: Human subjects research protections
- **HIPAA**: Health information privacy

### International

- **WHO Genomic Data Principles**: Ethical guidelines for human genomic data
- **Biological Weapons Convention**: Prohibits biological weapons development
- **IGSC Harmonized Screening Protocol**: Voluntary industry standard

### Australia

- **Biosecurity Act 2015**: Import risk analysis, compliance enforcement
- **Biosecurity Regulation 2016**: Operational requirements
- **BCAP**: Biosecurity Compliance Audit Program for poultry

---

## 12. Key Citations

1. Wittmann et al. (2025). "The limits of sequence-based biosecurity screening tools in the age of AI-assisted protein design." *Frontiers in Bioengineering and Biotechnology*.
2. NIST IR 8432 (2023). "Cybersecurity of Genomic Data." *NIST Technical Series*.
3. Zhou et al. (2024). "DNABERT-2: Efficient and Effective Bidirectional Encoder Representers from Transformers for Genomic Sequence Understanding."
4. Dalla-Torre et al. (2024). "Nucleotide Transformer v2: Building Genomic Foundation Models with Long-Range Context."
5. Brixi et al. (2026). "Evo 2: Long-context biological language modeling across domains of life."
6. National Academies of Sciences, Engineering, and Medicine (2025). "The Age of AI in the Life Sciences: Benefits and Biosecurity Considerations."
7. Pannu, J. (2026). "Shaping AI progress for biology and biosecurity." *Johns Hopkins Center for Health Security*.
8. Feldman, J. et al. (2026). "Know your scientist: KYC as biosecurity infrastructure." *Frontiers in Microbiology*.
9. WHO (2024). "Guidance for human genome data collection, access, use and sharing."
10. International Gene Synthesis Consortium (2024). "Harmonized Screening Protocol."

---

## Summary

Computational genomics biosecurity is at an inflection point. The democratization of AI-driven biological design (Evo, protein design tools) and decentralized DNA synthesis creates unprecedented dual-use risks. Current sequence-based screening is vulnerable to AI-designed synthetic homologs and adversarial perturbations. Governance frameworks (IGSC, NIH GDS, WHO) were designed for known pathogens and centralized synthesis, not the current landscape of open-weight models and benchtop synthesizers. Key technical needs include: (1) function-based rather than sequence-based screening, (2) adversarial-robust genomic foundation models, (3) international mandatory screening standards, and (4) privacy-preserving genomic data sharing mechanisms. The dual-mandate paradigm—building generation and defense capabilities in tandem—emerges as a promising approach for organizations with sufficient resources.
