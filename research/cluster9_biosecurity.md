# Cluster 9: AI/ML for Genomics — Biosecurity Research

**Date:** 2026-10-04
**Search queries:** 10 parallel web searches, top 3 results each (30 total)
**Focus:** Biosecurity governance, dual-use risk, frameworks, tools, hardware, cost, scalability, compliance

---

## 1. AI/ML for Genomics Biosecurity — State of the Art

AI models utilizing deep learning can now analyze genomic data rapidly to identify known pathogens, monitor genomic data continuously from various sources, and integrate genomic data with epidemiological information to predict outbreak patterns in near real time. The U.S. National Academies report *The Age of AI in the Life Sciences* (2025) frames the tension between discovery/acceleration and misuse, introducing the concept of AI-enabled capability uplift (ΔAI) — concluding that the strongest current uplift is in **ideation and design** while **experimental validation remains a major bottleneck**.

**Key finding:** More research in new methodologies for nucleic acid synthesis screening, including how to leverage AI-enabled biological tools for screening, is needed for this process to be an efficient control point.

### Top Results
1. **NCBI Bookshelf** — *Promoting and Protecting AI-Enabled Innovation for Biosecurity* (PMC9604978) — AI models for pathogen detection, biosurveillance, outbreak prediction. Calls for AI Safety Institute "if-then" strategy.
2. **NIST** — *A Call for Built-In Biosecurity Safeguards for Generative AI Tools* (Nature Biotechnology, 2025) — GenAI in biotechnology raises safety concerns; calls for AI-native safeguards (watermarking, alignment, anti-jailbreak, unlearning).
3. **MOZI.AI** — AI-based bioinformatics tools for genomics analytics and disease prediction.

---

## 2. AI Genomics Dual-Use

Dual-use capabilities of concern include: prediction/design of structural features constraining genetic changes; causal AI modeling of epidemiological spread; alteration of host range/tropism; increased resistance to therapeutics; and AI-enabled evasion of DNA synthesis screening. The PMC article *Dual-use capabilities of concern of biological AI models* argues that AI model evaluations should prioritize high-consequence risks (e.g., transmissible disease outbreaks) and that these risks should be evaluated **prior to model deployment**.

The *Trends in Genetics* safety-centric perspective (2026) explores how generative AI and foundation models for biological sequences can exacerbate data quality issues, technical biases, and dual-use potential — particularly in clinical genetics, precision medicine, and pathogen engineering. Key bottlenecks in the biorisk chain include **limited availability of biological datasets**, the **need for laboratory expertise**, and **restricted access to materials and infrastructure**.

### Top Results
1. **PMC** — *Dual-use capabilities of concern of biological AI models* (PMC12061118) — Categories of dual-use research mapped to emerging AI capabilities; pre-deployment evaluation framework.
2. **Trends in Genetics** — *A safety-centric perspective on innovation and risk in the use of AI in genomics* (2026) — Foundation models, bias, dual-use governance, EU AI Act classification as "high-risk."
3. **PubMed** — *A safety-centric perspective on innovation and risk* (PMID: 42062163) — Misuse risks throughout the innovation pipeline.

---

## 3. AI Genomics Ethics

A scoping review (Research Square, 2026) of AI-assisted genetic diagnosis ELSI identified six thematic clusters: (1) epistemic opacity and explainability illusion; (2) accountability and liability gaps; (3) genetic privacy and group harm; (4) bias, fairness, and genomic representativeness; (5) consent, autonomy, and reuse; (6) governance and regulation. **795 of 981 records (81%) failed the AI∩genomics∩ELSI intersection** at title/abstract level — the intersection is severely under-theorised.

The Nature article *Global patterns and gaps in AI policies of national genomics initiatives* reviewed 90 initiatives across 70 countries. Current or planned AI use was identified in 32/90 (36%), but **publicly available AI-specific governance policies were identified in only three initiatives in two countries**: All of Us, Genomics England, and UK Biobank. Three governance strategies recurred: mandatory secure computation environments, treatment of trained models as potentially disclosive data outputs, and restrictions on external generative AI services.

### Top Results
1. **Nature** — *Global patterns and gaps in AI policies of national genomics initiatives* (s44482-026-00043-5) — 90 initiatives, 70 countries; only 3 with AI-specific governance.
2. **Research Square** — *AI-Assisted Genetic Diagnosis and Its ELSI: A Scoping Review* — 6 thematic clusters; 81% gap at intersection.
3. **Cell / Trends in Genetics** — *A safety-centric perspective* — EU AI Act "high-risk" classification; bias in polygenic risk scores (15–20% accuracy loss in African groups).

---

## 4. Biosecurity Frameworks for AI Genomics

### KYC Framework (Frontiers in Microbiology, 2026)
A three-tier Know Your Customer framework inspired by anti-money laundering:
- **Tier I:** Research institutions as trust anchors vouching for affiliated researchers
- **Tier II:** Output screening through sequence homology searches and functional annotation
- **Tier III:** Behavioral pattern monitoring to detect anomalies

### Biosecurity Data Level (BDL) Framework (arXiv, 2026)
A five-tier framework for categorizing pathogen data by expected ability to contribute to capabilities of concern when used to train AI models. Each level has specific technical restrictions. Endorsed by 100+ researchers at the 50th anniversary Asilomar Conference.

### AI-Biosecurity Stack (Frontiers, 2026)
Extends the National Academies' capability uplift concept into a capability stack: risk and benefit emerge from connections among data, models, agents, laboratory automation, synthesis access, experimental validation, and governance. No single component determines risk independently.

### Top Results
1. **Frontiers in Microbiology** — *Know your scientist: KYC as biosecurity infrastructure* — Three-tier KYC framework.
2. **arXiv** — *Securing Dual-Use Pathogen Data of Concern* — Five-tier BDL framework; data controls as high-leverage interventions.
3. **Frontiers in Microbiology** — *From capability uplift to capability governance: an AI–biosecurity stack* — Capability stack approach; Evo 2 model.

---

## 5. AI Genomics Governance

The Nuffield Council on Bioethics / Ada Lovelace Institute joint project *AI and genomics futures* (final report, September 2024) concluded that the NHS should not widely roll-out AI-powered genomic health prediction technology yet. The project identified AI-powered genomic health prediction as an emerging area warranting urgent ethical consideration, with viability in the 5–10 year horizon.

The precautionary principle framework (PMC) proposes criteria for AI/ML-enabled genomics: reliability/accuracy/bias of predictions; benefit to individuals/society; scientific doubts about data quality; power asymmetries; general violation of fundamental human rights. The EU AI Act classifies AI-driven genomics applications as **'high-risk'**, mandating rigorous bias assessment, transparency, and risk management.

### Top Results
1. **Nuffield Council on Bioethics** — *AI and genomics futures* — Final report "Predicting: The future of health?" (Sept 2024).
2. **PMC** — *Regulating scientific and technological uncertainty* — Precautionary principle framework for AI/ML + genomics.
3. **Nuffield Council** — *The application of AI to genomics raises 'urgent' ethical questions* — Early findings (Aug 2023).

---

## 6. Biosecurity OSS Tools

- **IARPA Fun GCAT** (Functional Genomic and Computational Assessment of Threats): Multi-year research effort to develop new biosecurity tools to prevent accidental or intentional creation of biological threats.
- **Biosecurity Resource Toolbox** (International Biosafety): Six themes including dual-use framework, laboratory biosecurity guidance, DURC identification/assessment tools, vulnerability scans, self-assessment toolkits, and the Joint External Evaluation Tool (JEE).
- **BIO-ISAC Biosecurity Evaluation Questionnaire (BSEQ)**: Tool for evaluating OEM security practices in hardware/software lifecycle management within the bioeconomy.

### Top Results
1. **IARPA** — *Fun GCAT program* — Functional Genomic and Computational Assessment of Threats.
2. **International Biosafety** — *Biosecurity Resource Toolbox* — Six-theme resource collection.
3. **BIO-ISAC** — *Biosecurity Evaluation Questionnaire (BSEQ)* — Hardware/software security evaluation.

---

## 7. Biosecurity Hardware Requirements

The CASRAI Biosecurity Plan guide outlines eight required areas for a compliant biosecurity plan: risk assessment, access control (card/biometric), personnel suitability screening, inventory control (chain-of-custody logging), incident response, information systems security. The Federal Select Agent Program (FSAP) requires written security plans for any entity registered under 42 CFR 73.11, 7 CFR 331.11, or 9 CFR 121.11.

The BSEQ (Biosecurity Evaluation Questionnaire) from BIO-ISAC covers Organizational Security, General Product Security, Software Development Lifecycle (SDLC), and hosting-location-specific questions. *The Biosecurity Handbook* (Tegomoh) addresses biological security in the AI era.

### Top Results
1. **CASRAI** — *Biosecurity Plan: Elements & SRA Guide* — Eight required areas; FSAP compliance.
2. **Biosecurity Handbook** — *Biological Security in the AI Era* — Comprehensive handbook.
3. **BIO-ISAC** — *Biosecurity Evaluation Questionnaire (BSEQ)* — Hardware/software security evaluation tool.

---

## 8. Biosecurity Cost Analysis

- **Plant biosecurity** (PMC8365635): Costs split into prevention, surveillance/eradication, and established pest management. Economic approaches include cost accounting, partial equilibrium, and CGE modeling. Trade-offs exist between surveillance and eradication.
- **Poultry farms** (PMC3349596): Average preventive biosecurity cost was **3.55 eurocent per bird** for broilers (90% CI: 2.56–4.40) and **75.7 eurocent per bird** for hatching egg producers. For a batch of 75,000 broilers, total cost ≈ €2,700 (~2% of total production costs). Larger units incur lower per-bird costs.
- **Pig farming** (Frontiers, 2026): Systematic review of 586 publications (1995–2023). Biosecurity incurs upfront infrastructure costs but is offset by reduced disease losses. Cost-benefit ratios vary significantly by region, farm size, and disease prevalence. Adoption remains limited among small-scale producers.

### Top Results
1. **PMC** — *Approaches for estimating benefits and costs of interventions in plant biosecurity* — Economic modeling across invasion phases.
2. **PMC** — *Measuring the costs of biosecurity on poultry farms* — 3.55 eurocent/bird for broilers; 75.7 eurocent/bird for hatching eggs.
3. **Frontiers in Animal Science** — *The economic sustainability of biosecurity in pig farming* — Systematic review; 586 publications.

---

## 9. Biosecurity Scalability

The *Toward relational biosecurity* framework (Frontiers, 2026) argues for treating interactions between components as explicit objects of design and governance — system-level sensing, preservation of context and uncertainty, buffering of perturbations, and alignment with shared values across distributed actors.

DNA synthesis technology has evolved from chemical to enzymatic methods, from single-column to massively parallel chip-based approaches, and from a handful of commercial providers to a vast global market supplemented by decentralized benchtop systems. Oligonucleotide synthesis length increased from a few hundred bases in 2015 to **well over a thousand in 2026**. These advances have dramatically reduced costs while increasing the length of synthesizable oligonucleotides, making construction of large genetic constructs easier.

The AI-biosecurity stack framework highlights that governance is increasingly urgent at the interfaces of the stack — agentic AI, genome-scale foundation models, and self-driving laboratories make compositional workflows harder to oversee.

### Top Results
1. **Frontiers in Microbiology** — *Toward relational biosecurity* — System-level approach; interactions as objects of governance.
2. **Frontiers in Bioengineering** — *DNA synthesis technology evolution* — From chemical to enzymatic; massively parallel; >1000 bases in 2026.
3. **Frontiers in Microbiology** — *From capability uplift to capability governance* — AI-biosecurity stack; Evo 2; agentic AI.

---

## 10. Biosecurity Compliance

Biosecurity compliance was classified into four levels in a One Health modeling framework: **Excellent** (rigorous adherence with continuous monitoring), **Good** (most measures followed with minor lapses), **Marginal** (inconsistent adherence), and **Low** (practices largely neglected). Inconsistent implementation and monitoring remain significant challenges. Regulatory enforcement tends to emphasize penalties over educational support, complicating adherence.

The CASRAI framework distinguishes biosafety (containment to prevent accidental exposure) from biosecurity (access control, personnel reliability, material accountability to prevent deliberate misuse). In the US, the Federal Select Agent Program jointly administered by CDC and USDA-APHIS formalizes biosecurity for highest-consequence agents. DURC (Dual-Use Research of Concern) review adds an additional layer.

### Top Results
1. **Grokipedia** — *Biosecurity* — Comprehensive overview; defense-in-depth principle.
2. **PubMed** — *Assessing the impact of biosecurity compliance on farmworker and livestock health* — Four compliance levels; One Health framework.
3. **CASRAI** — *Biosafety vs. Biosecurity Explained* — Frameworks; FSAP; DURC review.

---

## Synthesis: Bottlenecks

1. **Experimental validation bottleneck** — AI capability uplift is strongest in ideation/design but experimental validation remains the major bottleneck (National Academies, 2025).
2. **Limited biological datasets** — Foundation models underperform due to lack of biological datasets, limiting both beneficial and harmful applications.
3. **Laboratory expertise requirement** — Credible misuse is largely confined to state-level or highly resourced actors with integrated biological capabilities.
4. **DNA synthesis screening gaps** — Current screening is not an efficient control point; more research needed on AI-enabled screening methodologies.
5. **Governance gap** — Only 3/90 national genomics initiatives have AI-specific governance policies; 81% of AI∩genomics∩ELSI literature fails the intersection.
6. **Data bias** — European individuals dominate genomic datasets; polygenic risk scores lose 15–20% accuracy in African groups.
7. **Model export/disclosure** — Trained models can leak participant data through membership inference or model inversion attacks.
8. **Cost barriers** — Biosecurity costs (e.g., 3.55 eurocent/bird) limit adoption among small-scale producers.
9. **Scalability of oversight** — Agentic AI, genome-scale models, and self-driving labs make compositional workflows harder to govern.
10. **Jurisdictional fragmentation** — No single regulation is enough; cross-border data sharing and model export complicate enforcement.

---

## Citations

1. Wang, M. et al. (2025). "A Call for Built-In Biosecurity Safeguards for Generative AI Tools." *Nature Biotechnology*, 43. https://doi.org/10.1038/s41587-025-02650-8
2. National Academies of Sciences, Engineering, and Medicine (2025). *The Age of AI in the Life Sciences: Benefits and Biosecurity Considerations*.
3. NCBI Bookshelf (2022). "Promoting and Protecting AI-Enabled Innovation for Biosecurity." PMC9604978.
4. PMC (2026). "Dual-use capabilities of concern of biological AI models." PMC12061118.
5. Trends in Genetics (2026). "A safety-centric perspective on innovation and risk in the use of artificial intelligence in genomics." PMID: 42062163.
6. Nature (2026). "Global patterns and gaps in AI policies of national genomics initiatives." https://doi.org/10.1038/s44482-026-00043-5
7. Research Square (2026). "AI-Assisted Genetic Diagnosis and Its Ethical, Legal and Social Implications: A Scoping Review."
8. Nuffield Council on Bioethics / Ada Lovelace Institute (2024). "Predicting: The future of health?" Final report.
9. PMC (2026). "Regulating scientific and technological uncertainty: The precautionary principle in the context of human genomics and AI." PMC11426231.
10. Frontiers in Microbiology (2026). "Know your scientist: KYC as biosecurity infrastructure." https://doi.org/10.3389/fmicb.2026.1814993
11. arXiv (2026). "Securing Dual-Use Pathogen Data of Concern." https://arxiv.org/pdf/2602.08061
12. Frontiers in Microbiology (2026). "From capability uplift to capability governance: an AI–biosecurity stack." https://doi.org/10.3389/fmicb.2026.1899413
13. IARPA (2018). "IARPA Launches Program to Develop New Biosecurity Tools" (Fun GCAT).
14. International Biosafety (2020). "Biosecurity Resource Toolbox."
15. BIO-ISAC. "Biosecurity Evaluation Questionnaire (BSEQ)."
16. CASRAI. "Biosecurity Plan: Elements & SRA Guide." https://casrai.org/guides/biosecurity-plan
17. Tegomoh, B. "The Biosecurity Handbook: Biological Security in the AI Era." https://biosecurityhandbook.com/biosecurity-handbook.pdf
18. PMC (2021). "Approaches for estimating benefits and costs of interventions in plant biosecurity across invasion phases." PMC8365635.
19. PMC (2012). "Measuring the costs of biosecurity on poultry farms." PMC3349596.
20. Frontiers in Animal Science (2026). "The economic sustainability of biosecurity in pig farming." https://doi.org/10.3389/fanim.2026.1738787
21. Frontiers in Microbiology (2026). "Toward relational biosecurity." https://doi.org/10.3389/fmicb.2026.1856819
22. Frontiers in Bioengineering and Biotechnology (2026). "DNA synthesis technology evolution." https://doi.org/10.3389/fbioe.2026.1819026
23. PubMed (2026). "Assessing the impact of biosecurity compliance on farmworker and livestock health." PMID: 40255412.
24. CASRAI. "Biosafety vs. Biosecurity Explained." https://casrai.org/dictionary/term/biosafety-and-biosecurity
