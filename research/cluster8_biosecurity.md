# Cluster 8: Epigenomics Biosecurity — Research Synthesis

**Date:** 2026-10-04  
**Focus:** Biosecurity implications of epigenomics technologies  
**Method:** 10 parallel web searches, top 3 results each, synthesized with bottlenecks and citations

---

## 1. Executive Summary

Epigenomics — the comprehensive study of chromatin constituents, gene regulation, and heritable phenotypic changes without DNA sequence alteration — sits at a critical biosecurity intersection. The convergence of AI-driven biological design, accessible DNA synthesis, and epigenetic editing technologies creates dual-use risks that existing governance frameworks are not equipped to address. This synthesis identifies key biosecurity gaps, governance frameworks, ethical concerns, and scalability challenges specific to epigenomics.

---

## 2. Biosecurity Governance

### 2.1 Current Framework Landscape

The regulatory architecture for epigenomics biosecurity is **fundamentally fragmented**:

- **NIH Guidelines**: Require Institutional Biosafety Committee (IBC) review for recombinant/synthetic nucleic acid research but offer **limited explicit coverage** for AI-driven design workflows or complex synthetic biology constructs.
- **WHO Laboratory Biosecurity Guidance**: Risk-based and comprehensive but **non-binding**, lacking enforceable global surveillance mechanisms.
- **EU Advanced Therapy Medicinal Product (ATMP) Regulation**: Centralized framework but **unevenly implemented** across member states; insufficient guidance for engineered synthetic circuits or AI-designed modifications.
- **FDA Gene Therapy Guidance**: Continues to evolve but remains **internationally inconsistent**.
- **ISO Standards for Stem Cell Biobanking**: Exist but **incompletely adopted**, particularly in lower-income settings.

### 2.2 Proposed Frameworks

**Biosecurity Data Levels (BDL) Framework** (Johns Hopkins Center for Health Security, 2026):
- Five-tier system for characterizing pathogen data based on expected ability to contribute to capabilities of concern when used to train AI models
- Anchors governance at the **data layer** — upstream intervention applicable to all AI models
- Recommends HHS guidelines for biological data governance, NIST technical standards, Trusted Research Environment (TRE) certification
- Key insight: data controls do not require coordination with AI model developers; safeguards persist even as AI capabilities evolve

**Adaptive Genomic Sovereignty Stewardship Model (AGSSM)**:
- Balances national data protection with international scientific collaboration
- Emphasizes responsible stewardship, controlled access, reciprocity, and adaptive governance
- Addresses the paradox that restrictive data policies can impede the science they aim to protect

**ICS Three-Level Action Proposals for Epigenomic Editing**:
- **Immediate**: FDA/EMA/China NHC should require "evidence excluding transgenerational epigenetic transmission" as mandatory approval element
- **Medium-term**: International epigenetic editing registry under WHO framework with mandatory cross-border clinical data sharing
- **Long-term**: Three-generation animal model data for germline-adjacent epigenetic editing research

### 2.3 Governance Gaps

- No integrated, real-time global biosafety registry for tracking adverse events across gene/cell therapy trials
- DURC governance frameworks not explicitly redesigned for AI-assisted biological design
- Multi-omics risk evaluation (transcriptomics, proteomics, metabolomics, immunogenicity) not standardized for capturing complex off-target effects
- Epigenetic editing approaching "Forbidden Red Lines" (FRL-1, FRL-3, FRL-4) without effective global governance response

---

## 3. Dual-Use Concerns

### 3.1 AI-Designed Biological Threats

- AI systems trained on large protein/genomic datasets can generate **novel amino acid sequences** with structural/functional properties similar to known hazardous proteins — but different enough to **evade similarity-based detection tools** used by DNA synthesis services
- This capability could lower time, expertise, and cost required to engineer dangerous biological phenotypes
- RAND/Helena January 2026 workshop identified three threat scenarios: novel influenza A release, agroterrorism targeting US wheat, state-sponsored insider attack using biofilm-forming bacterium

### 3.2 DNA Synthesis Supply Chain

- DNA synthesis has become so affordable and distributed that **traditional gatekeeping mechanisms no longer work**
- Provider screening varies significantly across vendors; much guidance is **voluntary and nonbinding**
- Agricultural pathogen screening receives less attention than human-pathogen screening

### 3.3 Epigenetic Editing-Specific Risks

- Epigenetic editing can alter gene expression without changing DNA sequence, potentially **evading sequence-based screening**
- Transgenerational epigenetic transmission raises concerns about **irreversible species-level effects**
- Consumer epigenetic testing (DTC-ET) companies commercialize biological age estimates without robust scientific validation
- Epigenetic data can reveal not just disease risk but **previous exposures and lifestyle** — more ethically sensitive than genetic data

### 3.4 Converging Dual-Use Domains

- Industrial bioproduction platforms could be redirected to manufacture harmful metabolites or toxins
- Gene-drive technologies raise environmental risks if unintended releases occur
- CRISPR-based genome editing: faster, cheaper, more accessible with obvious therapeutic benefits and equally obvious misuse potential

---

## 4. Ethics

### 4.1 Privacy and Identifiability

- Epigenetic data can be **equally "identifiable" as genetic data** — ethical concerns about public data availability
- Policies mandating data sharing may impede participant recruitment
- Epigenetic data reveals **previous exposures and lifestyle**, not just disease risk — potentially more ethically sensitive than genetic data
- Consent documents for biorepositories often not formulated broadly enough for epigenetic research

### 4.2 Discrimination and Equity

- Life insurance companies using epigenetic information widely viewed as ethically questionable (n=67 in international survey)
- Calls for legislation to prevent **epigenetic discrimination** approaching consensus
- High test costs reinforce health inequities
- "Epigenetic youth" narratives risk entrenching ageism
- Shifting responsibility for aging from structural conditions to individuals

### 4.3 Research Ethics

- 29.1% of researchers experienced ethical challenges accessing epigenetic data in existing databases
- 23.3% faced challenges obtaining ethics approval
- Practical and perceived overlap between genetics and epigenetics creates confusion for participants and ethics boards
- Broad consent for biorepositories has gained ethical acceptance but remains contested

### 4.4 Knowledge Translation

- Media communication identified as the **most important challenge** in ELSI knowledge translation
- Commercialization of epigenetic tests/products, intellectual property, and policymaking also raise ethical challenges
- Non-identity problem: philosophical conundrum of whether it is possible to harm someone who does not yet exist (relevant to transgenerational epigenetic effects)

---

## 5. Biosecurity OSS Tools

### 5.1 Detection and Surveillance

- **EPIWATCH**: Open-source AI platform leveraging machine learning to analyze public data sources for early epidemic detection; identifies outbreak signals before official alerts
- **Fun GCAT** (Functional Genomic and Computational Assessment of Threats): IARPA multi-year program to develop tools preventing accidental or intentional creation of biological threats
- **Biosecurity Resource Toolbox** (EBRF): Six-theme resource collection including laboratory biosecurity guidance, DURC identification/assessment tools, vulnerability scans, and self-assessment toolkits

### 5.2 Governance and Assessment Tools

- **GA4GH Regulatory Ethics Toolkit**: Harmonized governance tools for genomics adaptable for epigenomic research
- **EU STANDS4PM Data Access**: Framework for data access in personalized medicine
- **Joint External Evaluation Tool (JEE)**: WHO tool to assess country capacity to prevent, detect, and respond to public health threats
- **Laboratory Mapping Tool (LMT)**: For evidencing diagnostic laboratory gaps and strengths
- **Global Biorisk Management Curriculum (GBRMC)**: Based on CWA 15793 and WHO biosafety/biosecurity guidance

### 5.3 AI-Powered Tools

- **AlphaFold** (DeepMind): Structural prediction of viral proteins for threat assessment (2024 Nobel Prize in Chemistry)
- **BlueDot**: AI-based predictive analytics detecting unusual respiratory illness trends days before official alerts during COVID-19
- **AI "guardian models"**: Proposed for intent monitoring in AI-for-biology systems
- **BioTrust**: Proposed voluntary credentialing system modeled on ORCID for biosecurity

---

## 6. Hardware Requirements

### 6.1 Laboratory Containment

- **Biosafety Cabinets (BSC)**: Class II cabinets required for BSL-2 work; Class II Type B for chemical containment; Class II BSCs may be used with BSL-4 organisms in BSL-4 suit laboratories
- **HEPA Filtration**: Required for exhaust systems; bag-in/bag-out systems for hazardous chemical/radionuclide work
- **Facility Engineering**: Building exhaust systems, airtight dampers, clearance requirements (12-14 inches above cabinets), facility engineer consultation required

### 6.2 Physical Security

- **Access Control Systems**: Biometric scanners (fingerprint, facial recognition, palm vein), ID card readers, document scanners
- **Personnel Management**: Background-checked access logs, entry-control hardware
- **Inventory Tracking**: Chain-of-custody reconciliation for select agents
- **Perimeter Security**: Secure perimeters, visitor management systems, video surveillance (NVR/IPC systems)

### 6.3 Computational Infrastructure

- **Trusted Research Environments (TRE)**: Secure computing environments for sensitive biological data
- **High-Performance Computing**: For AI model training on genomic/epigenomic data
- **Secure Data Storage**: Federated cross-platform behavior analysis infrastructure

---

## 7. Cost Analysis

### 7.7 National Biosecurity Spending

- **Australia's biosecurity system**: $792.0M AUD total funding in 2023-24 ($379.1M cost recovery + $366.4M base appropriation + $46.5M STEPS program)
- Projected to grow to $841.1M AUD by 2024-25
- Cost recovery charges increased 3.8% in 2026-27 per legislated indexation
- New charges introduced for live snail consignments, vessel diagnostics

### 7.2 Technology Cost Drivers

- **DNA synthesis**: Costs have decreased dramatically, making gatekeeping increasingly difficult
- **AI model training**: Frontier models require significant compute investment
- **Biosafety cabinets**: Class II units with HEPA filtration, electrical consumption ~180W for new units
- **Autonomous labs**: Ginkgo Bioworks' Nebula platform represents significant capital investment in automated research infrastructure

### 7.3 Cost-Benefit Considerations

- **Ginkgo Bioworks divested biosecurity business** (April 2026), signaling market challenges in monetizing biosecurity
- Cost recovery models (import declarations, permit applications, quarantine charges) fund operational biosecurity
- Investment in AI safeguards, federated behavior analysis, and guardian models requires sustained funding

---

## 8. Scalability Limits

### 8.1 Framework Scalability

- **No one-size-fits-all approach**: Biosecurity implementation must be specific to local context and environment
- **Progressive Management Pathway for Terrestrial Animal Biosecurity (PMP-TAB)**: FAO stepwise approach for strengthening biosecurity along value chains
- **Geographic disparities**: Considerable disparities in evidence distribution and definitions hinder harmonious understanding
- **Single-disease focus**: Most biosecurity initiatives target single diseases in traditional livestock, failing to recognize wide range of hazards

### 8.2 Technology Scalability

- **AI guardian models**: Require cross-platform coordination and information sharing between LLM companies
- **Federated behavior analysis**: Needs cross-platform infrastructure that doesn't yet exist at scale
- **Synthetic DNA screening**: Agricultural pathogen screening less developed than human-pathogen screening
- **Autonomous labs**: Ginkgo targeting to double Nebula platform size, but "large market remains overwhelmingly manual"

### 8.3 Governance Scalability

- **96 countries surveyed**: 75 prohibit reproductive genome editing to some degree, only 11 explicitly permit non-reproductive germline research, 23 in ambiguous status
- **Bilateral/multilateral data sharing**: Major markets (EU, US, China) can pioneer without awaiting global consensus
- **Regulatory fragmentation**: Patchwork of national/international frameworks creates compliance complexity for multinational research

---

## 9. Compliance

### 9.1 Regulatory Compliance

- **Federal Select Agent Program** (CDC/USDA-APHIS): Requires written security plan, restricted/logged access, personnel suitability screening, inventory reconciliation
- **DURC Review**: Institutional Review Entity (IRE) conducts dual-use risk-mitigation review layered on standard biosafety
- **NIH Guidelines**: IBC review required for recombinant/synthetic nucleic acid research
- **OSHA Bloodborne Pathogen Standard**: Applies alongside biosafety controls

### 9.2 Compliance Challenges

- **Farm-level compliance**: Inconsistent implementation and monitoring; effectiveness varies widely; lack of standardized assessment tools
- **Regulatory enforcement**: Tends to emphasize penalties over educational support, reducing compliance
- **Veterinary guidance**: Inconsistent guidance and poor communication between stakeholders leads to distrust
- **Data sharing**: Lack of standardized mechanisms complicates compliance evaluation

### 9.3 Compliance Framework Components

- Biosafety + Biosecurity = complete program (containment + accountability)
- IBC oversight for biosafety; Federal Select Agent Program for biosecurity
- Regular inspections verify plans match actual practice (access lists, inventory reconciliation, entry-control hardware)
- Quantity-specific exemptions (42 CFR 73.6) remove Select Agent Program obligations but not NIH Guidelines/BMBL requirements

---

## 10. Bottlenecks

1. **Regulatory lag**: Pace of innovation has decisively outrun coordination of governance
2. **Detection evasion**: AI-designed novel proteins evade similarity-based screening tools
3. **Data governance gap**: No enforcement authority over preparation, training, and deployment of AI systems using high-consequence biological data
4. **Fragmented frameworks**: Patchwork of national/international regulations with inconsistent enforcement
5. **Consent/ethics bottleneck**: Existing consent documents and biorepository agreements not designed for epigenetic research
6. **Transgenerational uncertainty**: No framework for assessing or requiring evidence excluding transgenerational epigenetic transmission
7. **Agricultural pathogen screening**: Less developed than human-pathogen screening
8. **Cross-platform coordination**: No infrastructure for federated behavior analysis or information sharing between LLM companies
9. **Cost sustainability**: Biosecurity business models struggle (Ginkgo divestiture signals market challenges)
10. **Standardization**: Lack of standardized assessment tools for biosecurity compliance evaluation

---

## 11. Failure Modes

1. **AI-generated biological threats**: Novel pathogens/toxins designed by AI evade existing detection
2. **Epigenetic editing misuse**: Transgenerational effects released without adequate safety assessment
3. **DNA synthesis screening failure**: Dangerous sequences ordered from unscrupulous or screening-incapable vendors
4. **Data breach**: Sensitive epigenetic data exposed, revealing individual exposure/lifestyle information
5. **Autonomous lab misuse**: AI-driven biological discovery systems used for weapon design
6. **Regulatory arbitrage**: Research moved to jurisdictions with weaker oversight
7. **False negative in screening**: Similarity-based tools fail to flag AI-designed hazardous sequences
8. **Consent violation**: Epigenetic data used beyond original consent scope
9. **Inventory discrepancy**: Select agent inventory records don't match physical reality
10. **Compliance theater**: Security plans exist on paper but don't match actual practice

---

## 12. NP-Hard Problems

1. **Optimal biosecurity resource allocation**: Distributing limited screening/containment resources across global DNA synthesis supply chain is computationally intractable
2. **AI intent classification**: Determining whether a prompt sequence represents malicious intent vs. legitimate research is undecidable in general
3. **Epigenetic off-target prediction**: Predicting all downstream effects of epigenetic modifications across cell types, developmental stages, and generations
4. **Multi-omics risk integration**: Combining transcriptomic, proteomic, metabolomic, and epigenomic data for holistic risk assessment
5. **Federated threat detection**: Coordinating detection across platforms without centralizing sensitive data
6. **Transgenerational effect modeling**: Predicting epigenetic inheritance patterns across multiple generations

---

## 13. Most Cited Papers

1. **Wang KC (2018)** — "Epigenomics: Technologies and Applications" — Cited by 189 — Comprehensive review of high-throughput epigenome mapping technologies and multi-omics integration
2. **Dupras C, Saulnier KM, Joly Y (2019)** — "Epigenetics, ethics, law and society: A multidisciplinary review" — PMC6801799 — Nine areas of discussion at crossroads of epigenetics, ethics, law and society
3. **Pannu J (2026)** — "Shaping AI progress for biology and biosecurity" (3-part series) — Johns Hopkins Center for Health Security — AI compressing decades of research into years; autonomous biological discovery; smallpox eradication analogy
4. **Zhan A (2026)** — "Revolutionizing biosecurity: new multi-omics framework" — Biological Diversity — Proactive, predictive, integrative framework for invasive species management
5. **RAND/Helena (2026)** — "AI-enabled biological threats workshop proceedings" — Three threat scenarios with mitigation strategies

---

## 14. SOTA Approaches

1. **Biosecurity Data Levels (BDL)**: Five-tier risk categorization for biological data used in AI training
2. **AI Guardian Models**: LLM-based intent monitoring and de-escalation (adapted from suicide prevention techniques)
3. **BioTrust Credentialing**: Voluntary ORCID-modeled system for researcher vetting
4. **Multi-Omics Risk Evaluation**: Integrated transcriptomic/proteomic/metabolomic/immunogenicity profiling
5. **EPIWATCH**: Open-source AI early epidemic detection from public data
6. **Autonomous Lab Integration**: AI systems automating full research cycle (Isomorphic Labs, FutureHouse, Ginkgo Nebula)
7. **Federated Cross-Platform Behavior Analysis**: Proposed infrastructure for detecting malicious patterns without centralizing data
8. **Synthetic DNA Screening**: Sequence similarity-based detection (current standard, increasingly insufficient)
9. **Transgenerational Safety Assessment**: Proposed three-generation animal model data requirement
10. **International Epigenetic Editing Registry**: Proposed WHO-framework cross-border clinical data sharing

---

## 15. Hardware Requirements Summary

| Category | Requirements |
|----------|-------------|
| Containment | BSC Class II (HEPA filtration, ~180W), BSL-1 through BSL-4 facilities |
| Physical Security | Biometric access control, inventory tracking, perimeter security, NVR/video surveillance |
| Computational | TRE secure computing, HPC for AI training, federated analysis infrastructure |
| Sequencing | High-throughput epigenome mapping (bisulfite-seq, ChIP-seq, ATAC-seq, Hi-C) |
| Decontamination | Formaldehyde gas systems, bag-in/bag-out HEPA replacement, autoclaves |

---

## 16. Cost Tradeoffs

| Approach | Cost | Benefit | Tradeoff |
|----------|------|---------|----------|
| DNA synthesis screening | Moderate | Catches known threats | Misses AI-designed novel sequences |
| AI guardian models | High compute | Intent monitoring | False positives may impede legitimate research |
| Autonomous labs | Very high capital | 24/7 research throughput | Dual-use risk if misused |
| BSL-3/4 facilities | Very high | Maximum containment | Limits research accessibility |
| Federated analysis | Moderate | Privacy-preserving coordination | Complex implementation |
| International registry | Low-moderate | Cross-border transparency | Sovereignty concerns |
| Multi-omics profiling | High | Comprehensive off-target detection | Expensive per sample |

---

## 17. Citations

1. Pannu J. "Five Things (May 23, 2026): AI in life sciences." Johns Hopkins Center for Health Security. https://doi.org/10.59350/8103y-x2w56
2. Global Biodefense (2026). "CRISPR, AI, and Accessible DNA Synthesis Are Outpacing Global Biosecurity Oversight." Journal of Biosafety and Biosecurity. https://globalbiodefense.com/2026/06/17/gene-editing-and-synthetic-biology-are-outpacing-global-biosecurity-regulation-new-review-warns
3. Emerging technologies transforming the future of global biosecurity (2026). PMC12174072. https://pmc.ncbi.nlm.nih.gov/articles/PMC12174072
4. Wang KC (2018). "Epigenomics: Technologies and Applications." PubMed 29700067. https://pubmed.ncbi.nlm.nih.gov/29700067
5. Epigenomics—Technologies and Applications (2018). PMC5929475. https://pmc.ncbi.nlm.nih.gov/articles/PMC5929475
6. "The Ghost in Our Genes: Legal and Ethical Implications of Epigenetics." PMC3034450. https://pmc.ncbi.nlm.nih.gov/articles/PMC3034450
7. Researcher perspectives on ethics considerations in epigenetics (2022). PMC9440515. https://pmc.ncbi.nlm.nih.gov/articles/PMC9440515
8. Dupras C, Saulnier KM, Joly Y (2019). "Epigenetics, ethics, law and society." PMC6801799. https://pmc.ncbi.nlm.nih.gov/articles/PMC6801799
9. Center for Health Security (2026). "Risk-Based Categorization and Governance of Biological Data in AI Systems." https://centerforhealthsecurity.org/sites/default/files/2026-03/Biological-Data-Governance-Framework.pdf
10. Zhan A (2026). "Revolutionizing biosecurity: new multi-omics framework." Biological Diversity. https://www.eurekalert.org/news-releases/1111714
11. Consumer epigenomics and biological age editing (2026). Springer. https://link.springer.com/article/10.1186/s43682-026-00044-8
12. "The National Genome Sovereignty in a Global Genomics Ecosystem." IntechOpen. https://intechopen.com/chapters/1249173
13. "The Civilizational Threshold of Epigenomic Editing." ICS. https://ics-studies.org/en/research-archive/epigenomic-editing-2026.html
14. IARPA (2018). "IARPA Launches Program to Develop New Biosecurity Tools." https://www.iarpa.gov/newsroom/article/iarpa-launches-program-to-develop-new-biosecurity-tools
15. Biosecurity Resource Toolbox (2020). EBRF. https://internationalbiosafety.org/wp-content/uploads/2020/12/Biosecurity-resource-toolbox_v7_EBRF-2020.pdf
16. Primary Containment for Biohazards (3rd Edition). APSU. https://www.apsu.edu/health-safety/Primary_containment_for_biohazards.pdf
17. Australia DAFF (2024). "Biosecurity Funding and Expenditure Report 2023-24." https://www.agriculture.gov.au/sites/default/files/documents/biosecurity-funding-expenditure-report-2023-24.pdf
18. Australia DAFF (2026). "Fees and charges for biosecurity 2026-27." https://www.agriculture.gov.au/sites/default/files/documents/2026-27-fees-charges.pdf
19. Characterising Biosecurity Initiatives Globally (2023). PMC10451226. https://pmc.ncbi.nlm.nih.gov/articles/PMC10451226
20. Ginkgo Bioworks (2026). "Q1 2026 Financial Results, Completes Divestiture of Biosecurity." SEC Filing. https://www.sec.gov/Archives/edgar/data/1830214/000162828026032093/ex991earningspr.htm
21. Grokipedia. "Biosecurity." https://grokipedia.com/page/Biosecurity
22. Assessing biosecurity compliance impact (2024). PubMed 40255412. https://pubmed.ncbi.nlm.nih.gov/40255412/
23. CASRAI. "Biosafety vs. Biosecurity Explained." https://casrai.org/dictionary/term/biosafety-and-biosecurity

---

## 18. Key Takeaways

1. **Epigenomics biosecurity is an emerging frontier** — existing frameworks were designed for physical materials and sequence-based detection, not AI-driven epigenetic design
2. **The BDL framework** offers the most promising governance approach by anchoring controls at the data layer
3. **AI-designed proteins evading detection** is the most acute near-term threat
4. **Transgenerational epigenetic effects** represent a potentially irreversible risk category requiring new regulatory approaches
5. **Cost sustainability** is a structural challenge — even well-funded programs (Ginkgo) have divested biosecurity businesses
6. **International coordination** remains the fundamental bottleneck — no enforceable global surveillance mechanism exists
7. **Epigenetic data privacy** is more complex than genetic data privacy due to exposure/lifestyle information content
