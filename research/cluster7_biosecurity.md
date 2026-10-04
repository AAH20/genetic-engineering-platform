# Cluster 7: Single-Cell Genomics Biosecurity

## Overview

Single-cell genomics biosecurity encompasses the intersection of high-resolution single-cell technologies (scRNA-seq, scATAC-seq, spatial transcriptomics) with biosecurity governance, data privacy, dual-use risk, and responsible innovation. As single-cell datasets scale to millions of cells and population-level atlases, new vulnerabilities emerge: linking attacks on donor privacy, AI-enabled design of pathogenic proteins, and the need for data-level controls on dual-use pathogen information.

---

## 1. Single-Cell Genomics Biosecurity

### Key Findings

- **Dual-use pathogen data controls**: An international group of 100+ researchers at the 50th anniversary Asilomar Conference endorsed a five-tier Biosecurity Data Level (BDL) framework for categorizing pathogen data based on its expected ability to contribute to capabilities of concern when used to train AI models. Each tier proposes technical restrictions appropriate to its risk level. The framework argues that data controls may be among the most high-leverage interventions to reduce proliferation of concerning biological AI capabilities. [1]

- **AI-for-biology biosecurity**: AI systems are compressing decades of biological research into years. The same systems that enable cures can lower the barrier to weaponizing pathogens. Autonomous biological discovery systems (e.g., Isomorphic Labs, FutureHouse, Ginkgo Bioworks) automate every step of the research cycle. AI-driven design can explore biological space that nature has not, without fitness valley constraints. [2]

- **Mosquito single-cell applications**: scRNA-seq is rewriting mosquito biology, exposing cell types and host–pathogen interactions relevant to disease transmission. The technical pipeline (tissue dissociation, cell capture, library prep, sequencing) has biosecurity implications when applied to vector species. [3]

### Citations

[1] "Securing Dual-Use Pathogen Data of Concern" — arXiv:2602.08061
[2] "Five Things (May 23, 2026): AI in life sciences" — doi.org/10.59350/8103y-x2w56
[3] "Single-cell RNA sequencing reveals hidden cell types shaping mosquito disease transmission" — Scienmag/Parasites & Vectors

---

## 2. Single-Cell Data Privacy

### Key Findings

- **Linking attacks on single-cell data**: A study published in *Cell* (Oct 2024) by Gamze Gürsoy et al. (Columbia University/NYGC) demonstrated that individuals in single-cell gene expression datasets are vulnerable to "linking attacks." Hackers can uncover private genetic and physical trait information of research participants using publicly available information only. The attack works even when eQTL data is unavailable, by leveraging genetic and single-cell data from a smaller cohort to train a predictive model. [4]

- **Cross-cohort privacy leakage**: The ability to leverage data generated in a different lab, processed with a different method, to link individuals in a completely different anonymous dataset highlights a real privacy issue. Healthy datasets can be used to predict information about diseased datasets because there are enough underlying commonalities within gene expressions of healthy and diseased individuals. [4]

- **Consent and policy implications**: The study aims to help quantify risks before data release and shape the design of future studies, consent policies, and legislation preventing attackers from using this information for harm. [4]

- **Platform privacy practices**: The Broad Institute Single Cell Portal stores user information (Google profiles, email, OAuth tokens) with 256-bit AES encryption at rest. Publicly uploaded studies are accessible by third parties. The portal does not sell user information but disclaims liability for third-party misuse. [5]

### Citations

[4] "New Method Quantifies Single-Cell Data's Risk of Private Information Leakage" — Columbia DBMI, *Cell* (2024)
[5] "Privacy policy - Single Cell Portal" — Broad Institute
[6] "Unveiling the risks: protecting privacy in single-cell genomics data" — *Nephrol Dial Transplant* 2025;40(6):1077-1080

---

## 3. Single-Cell Data Sharing

### Key Findings

- **PSCS (Platform for Single-Cell Science)**: A web platform enabling no-code analysis pipeline design, computing, and sharing of entire data analysis pipelines, input data, and interactive results as a unit. Integrates Scanpy, CAPITAL, MiloPy, and scTransient. Uses Annotated Data format for interoperability. Projects encapsulate data, analyses, and results with version control. [7]

- **Human Cell Atlas (HCA) Data Portal**: A public, cloud-based platform where scientists share, organize, and interrogate single-cell data. Strategic aims include maximizing data value, enabling fundamental biology answers, regular data releases, computational method alignment, and community standards for experimental design. [8]

- **Broad Institute Single Cell Portal**: Accepts AnnData (.h5ad) files to power visualizations, bridging the gap between analysis files and shared data. Supports both classic multi-file upload and single AnnData object upload. [9]

### Citations

[7] "PSCS: Unified Sharing of Single-Cell Omics Data, Analyses, and Results" — PMC12831219
[8] "About the HCA Data Portal" — data.humancellatlas.org
[9] "Single Cell Portal Now Accepts AnnData Files" — Broad Institute (May 2023)

---

## 4. Biosecurity Frameworks for Single-Cell

### Key Findings

- **Hybrid governance framework**: A Delphi process with 13 experts identified consistent biological threat prioritizations and established consensus-driven policy recommendations. The framework has four sequential components: (1) raising awareness, (2) establishing robust training and monitoring systems, (3) developing agile governance frameworks, and (4) strengthening international treaties (BWC). [10]

- **NIH Guidelines and IBC oversight**: Institutional Biosafety Committees (IBCs) ensure appropriate containment practices and compliance with NIH Guidelines. Risk assessment considers: whether components can replicate or persist, whether expressed products include toxins, routes of exposure, expected dose/frequency, environmental fate, and decontamination availability. [11]

- **National Academies framework**: The "Biodefense in an Age of Synthetic Biology" study produced a framework for assessing risk of engineering biological capabilities, building on the 2004 "Biotechnology in an Age of Terrorism" report. Key triggers: recreation of poliovirus (2002), first synthetic cell, first CRISPR use in humans. [12]

### Citations

[10] "Improving governance in the age of synthetic biology, artificial intelligence, and diverging threats" — *Frontiers in Bioengineering and Biotechnology* (2026)
[11] "Cases Across the Continuum: Biosafety, Biosecurity, and Environmental Considerations" — NCBI/NAP29325
[12] "Biosecurity Assessments for Emerging Transdisciplinary Biotechnologies" — PMC11447134

---

## 5. Single-Cell Ethics

### Key Findings

- **Stem cell ethics**: The main ethical objection to embryonic stem cell (HESC) research is the destruction of human embryos. Induced pluripotent stem cells (iPSCs) bypass this issue but raise questions about complicity, moral status of embryos, and the distinction between active and passive potential. [13, 14]

- **Synthetic cell ethics**: Creating artificial cells raises bioethical questions about the nature of life, human responsibility, reductionism (loss of distinction between living organisms and machines), and the precautionary principle. [15]

- **Regenerative medicine ethics**: Informed consent, intellectual property, conflicts of interest, and the need for global regulations to protect patients from unregulated stem cell clinics. [13]

### Citations

[13] "Science and ethics: bridge to the future for regenerative medicine" — PMC3840959
[14] "Ethics of Stem Cell Research" — Stanford Encyclopedia of Philosophy (Spring 2026)
[15] "Synthetic Cells and Their Ethical Implications" — Bioethics Observatory (July 2026)

---

## 6. Biosecurity OSS Tools

### Key Findings

- **Sequence-based biosecurity screening vulnerabilities**: AI-assisted protein design (AIPD) tools can evade biosecurity screening software (BSS) used by nucleic acid synthesis providers. Synthetic homologs with minimal sequence identity to wild-type proteins of concern can fold into structurally similar proteins, potentially retaining hazardous function. Four BSS tools were tested; two detected fragments as short as 50 nucleotides. [16, 17]

- **Protein watermarking**: Google DeepMind published a system creating watermarks on protein sequences without compromising function, based on SynthID technology. This allows AI-designed proteins from trusted researchers to be identified, enabling closer scrutiny of unmarked sequences. [18]

- **Relational biosecurity framework**: A perspective arguing for treating interactions between components as explicit objects of design and governance, emphasizing system-level sensing, preservation of context, buffering of perturbations, and alignment with shared values across distributed actors. [19]

### Citations

[16] "The limits of sequence-based biosecurity screening tools in the age of AI-assisted protein design" — *Frontiers in Bioengineering and Biotechnology* (2026)
[17] "The Limits of Sequence-Based Biosecurity Screening Tools in the Age of AI-Assisted Protein Design" — bioRxiv (2026)
[18] "Google figures out how to watermark AI-designed proteins" — Ars Technica (Sept 2026)
[19] "Toward relational biosecurity: understanding AI-enabled biology as a connected system" — *Frontiers in Microbiology* (2026)

---

## 7. Biosecurity Hardware Requirements

### Key Findings

- **Biological safety cabinets (BSCs)**: Class II BSCs provide personnel, environmental, and product protection. Key specs: HEPA filtration, measured airflow certification, electrical consumption ≤180W for new units. Class II Type B cabinets originated with the National Institutes of Health. BSCs are only part of an overall biosafety program requiring good microbiological practices and proper facility design. [20, 21]

- **Primary containment requirements**: Adequate clearance behind and on each side of cabinets, 12-14 inch clearance above for air velocity measurement. Bag-in/bag-out systems for hazardous chemicals or radionuclides. HEPA filters must be decontaminated before removal. [21]

- **Physical biosecurity hardware**: Access control systems (fingerprint, facial recognition, card readers), ID document scanners, QR code scanners, and integrated security management platforms for personnel/visitor management. [22]

### Citations

[20] "Biological safety cabinets - Thermo Fisher Scientific" — Thermo Fisher bid specs
[21] "Primary Containment for Biohazards: Selection, Installation and Use of Biological Safety Cabinets 3rd Edition" — APSU
[22] "ZKBioSecurity Hardware Suggestion List" — ZKTeco

---

## 8. Biosecurity Cost Analysis

### Key Findings

- **Australian biosecurity funding**: Total biosecurity funding for 2023-24 was $792.0M AUD, comprising $379.1M cost recovery and $366.4M base appropriation. Forward estimates project $811.3M by 2027-28. Cost recovery includes self-assessed clearances, Australia Post, Defence, and other s74 contract revenue. [23]

- **Cost recovery charges**: Import declaration charges ($46-71), permit applications ($130-135), animal reservation charges ($269-$4,447 depending on species). Fees increased 3.8% in 2026-27 per legislated indexation. [24]

- **Biosecurity services market**: Companies like Biosecurity BV provide hygiene scans, risk management tools, and cleaning/disinfection products for agriculture and human health. [25]

### Citations

[23] "Biosecurity Funding and Expenditure Report 2023-24" — Australian DAFF
[24] "Fees and charges for biosecurity and imported food regulatory activity 2026-27" — Australian DAFF
[25] "Biosecurity BV" — Tracxn company profile

---

## 9. Biosecurity Scalability

### Key Findings

- **DNA synthesis evolution**: Since the 1980s, DNA synthesis has evolved from chemical to enzymatic methods, from single-column to massively parallel chip-based approaches. Oligonucleotide length increased from a few hundred bases (2015) to over 1000 (2026). Longer oligonucleotides combined with improved assembly methods have made construction of large genetic constructs easier, challenging list-based biosecurity approaches. [26]

- **AI-biosecurity stack**: Risk and benefit emerge from connections among data, models, agents, laboratory automation, synthesis access, experimental validation, and governance. No single component determines risk independently. The concept of AI-enabled capability uplift (ΔAI) frames the strongest current uplift in ideation and design, with experimental validation remaining a major bottleneck. [27]

- **Relational biosecurity at scale**: System-level objectives must be represented, measured, and propagated across components to enable coherent oversight of compositional workflows. This extends existing safeguards by addressing how they interact within workflows. [19]

### Citations

[26] "Improving governance in the age of synthetic biology, artificial intelligence, and diverging threats" — *Frontiers in Bioengineering and Biotechnology* (2026)
[27] "From capability uplift to capability governance: an AI–biosecurity stack" — *Frontiers in Microbiology* (2026)
[19] "Toward relational biosecurity" — *Frontiers in Microbiology* (2026)

---

## 10. Biosecurity Compliance

### Key Findings

- **Australian Biosecurity Act 2015**: Comprehensive legislation covering human biosecurity control orders, traveller movement measures, isolation measures, compliance and enforcement powers, and ballast water management. Biosecurity officers have powers to secure vessels, inspect and take samples, and enforce compliance through civil penalties, infringement notices, and injunctions. [28, 29]

- **Biosecurity Compliance Audit Program (BCAP)**: California poultry producers must pass biosecurity audits to receive indemnity payments for HPAI. Audits review biosecurity plans, perimeter security, line of separation, rodent/wildlife control, employee training records, and movement tracking. Virtual and in-person audits required. [30]

- **Regulatory framework**: The Biosecurity Regulation 2016 covers import risk analyses, approved arrangements, monitoring/control/response, and compensation for destroyed animals/goods. [29]

### Citations

[28] "Biosecurity Act 2015" — Australian Legislation
[29] "Biosecurity Regulation 2016" — Australian Legislation
[30] "Biosecurity Compliance Audit Program (BCAP)" — CDFA/USDA APHIS (2025)

---

## Bottlenecks

1. **Linking attack vulnerability**: Single-cell data cannot be fully anonymized; cross-cohort linking attacks can re-identify individuals using only public data, requiring new privacy-preserving technologies and consent frameworks.

2. **Sequence-based screening evasion**: AI-assisted protein design can generate sequence-divergent homologs that evade current biosecurity screening software, necessitating function-prediction-based screening approaches.

3. **Data sharing vs. privacy tension**: Platforms like HCA and Single Cell Portal enable scientific progress but create attack surfaces for privacy breaches. Balancing open science with donor protection remains unresolved.

4. **Governance lag**: Biosecurity frameworks (NIH Guidelines, BWC) were designed for state-centric bioweapons programs and struggle to address decentralized, AI-enabled, dual-use research by non-state actors.

5. **Scalability of compliance**: As single-cell datasets scale to millions of cells and population-level atlases, manual compliance review becomes infeasible. Automated, scalable biosecurity screening is needed.

6. **Hardware-software integration**: Physical containment (BSCs, access control) and digital biosecurity (sequence screening, data access controls) operate in silos; integrated systems are needed for comprehensive biosecurity.

7. **Cost of compliance**: Biosecurity audits, containment infrastructure, and compliance programs impose significant costs (e.g., Australia's $792M annual biosecurity budget), creating barriers for smaller institutions and researchers.

8. **International coordination**: Biosecurity threats are national but governance is fragmented across jurisdictions (Australian Biosecurity Act, US NIH Guidelines, BWC), creating gaps in enforcement and information sharing.

---

## Summary

Single-cell genomics biosecurity is an emerging field at the intersection of high-resolution genomics, AI, and biosecurity governance. Key challenges include protecting donor privacy against linking attacks, preventing AI-enabled evasion of sequence-based screening, scaling compliance for population-level datasets, and modernizing governance frameworks designed for state-centric bioweapons programs. The field requires integrated approaches combining technical controls (watermarking, privacy-preserving computation), governance innovation (BDL framework, relational biosecurity), and international cooperation.
