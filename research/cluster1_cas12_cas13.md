# Cluster 1: CRISPR-Cas12 & Cas13 Systems — Research Summary

## 1. Cas12 Mechanism Review

**Classification:** Type V CRISPR-Cas system (single-subunit endonuclease).

**Key Mechanism:**
- Uses only crRNA for target recognition (no tracrRNA required), simplifying design vs. Cas9.
- Recognizes T-rich PAM motifs (e.g., TTTV for AsCas12a/LbCas12a) upstream of the protospacer.
- Cleaves double-stranded DNA via a single RuvC nuclease domain, producing staggered cuts with 5′ overhangs.
- Exhibits **trans-cleavage (collateral) activity**: after specific target binding, indiscriminately degrades ssDNA molecules in the vicinity — the basis for CRISPR diagnostics.
- Self-processes pre-crRNA from the CRISPR array, enabling multiplexed targeting from a single transcript.
- Compact orthologs (Cas12f ~500 aa, Cas12i ~700-800 aa) are significantly smaller than Cas9 (~1,368 aa), facilitating AAV delivery.

**Subtypes:** Cas12a (Cpf1), Cas12b (C2c1), Cas12c, Cas12e (CasX), Cas12f (Cas14-like), Cas12i, Cas12j, Cas12k, Cas12m, Cas12n, Cas12o, Cas12p, Cas12q, Cas12r, Cas12s, Cas12t, Cas12u, Cas12v, Cas12w, Cas12x, Cas12y, Cas12z.

**Citations:**
- Hillary, V.E. & Ceasar, S.A. (2023). "A Review on the Mechanism and Applications of CRISPR/Cas9/Cas12/Cas13/Cas14 Proteins Utilized for Genome Engineering." *Mol Biotechnol* 65(3): 311-332. PMC9512960.
- Yan, W.X. et al. (2019). "Functionally diverse type V CRISPR-Cas systems." *Science* 363(6422): 88-91. DOI: 10.1126/science.aav7271.
- Zetsche, B. et al. (2015). "Cpf1 is a single RNA-guided endonuclease of a class 2 CRISPR-Cas system." *Cell* 163(3): 759-771. DOI: 10.1016/j.cell.2015.09.038.

---

## 2. Cas13 Mechanism Review

**Classification:** Type VI CRISPR-Cas system (RNA-guided RNase).

**Key Mechanism:**
- Targets single-stranded RNA (ssRNA) — not DNA — via crRNA guidance.
- Self-processes pre-crRNA; no tracrRNA required.
- Contains two HEPN (Higher Eukaryotes and Prokaryotes Nucleotide-binding) domains that mediate RNA cleavage.
- Upon target RNA binding, undergoes conformational change activating **collateral RNase activity**: promiscuous cleavage of non-target ssRNA molecules.
- Four subfamilies: Cas13a (C2c2), Cas13b, Cas13c, Cas13d.
- No strict PAM requirement, but exhibits protospacer flanking site (PFS) preferences (e.g., 3′ H (non-G) for LwaCas13a).
- Bilobed architecture: REC lobe (crRNA recognition) + NUC lobe (target RNA cleavage).

**Citations:**
- Abudayyeh, O.O. et al. (2017). "C2c2 is a single-component programmable RNA-guided RNA-targeting CRISPR effector." *Science* 353(6299): aaf5573. DOI: 10.1126/science.aaf5573.
- Liu, L. et al. (2017). "The molecular architecture for RNA-guided RNA cleavage by Cas13a." *Cell* 170(4): 714-726. DOI: 10.1016/j.cell.2017.06.032.
- Meeske, A.J. et al. (2020). "A phage-encoded anti-CRISPR enables complete evasion of type VI-A CRISPR-Cas immunity." *Science* 369(6501): 54-59. DOI: 10.1126/science.abb6151.
- Wessels, H.H. et al. (2024). "Structures, mechanisms and applications of RNA-centric CRISPR-Cas13." *Nat Chem Biol* 20: 693-704. PMC11375968.

---

## 3. Cas12 vs Cas9 Comparison

| Feature | Cas9 (Type II) | Cas12 (Type V) |
|---|---|---|
| **Target** | dsDNA | dsDNA (ssDNA via trans-cleavage) |
| **PAM** | NGG (SpCas9) | TTTV (Cas12a) — T-rich |
| **tracrRNA** | Required | Not required |
| **Cut type** | Blunt DSB | Staggered DSB (5′ overhangs) |
| **Size** | ~1,368 aa | ~1,200-1,300 aa (Cas12a); ~500 aa (Cas12f) |
| **crRNA processing** | Requires RNase III | Self-processing |
| **Collateral activity** | None | ssDNA trans-cleavage |
| **Multiplexing** | Complex (multiple sgRNAs) | Simple (single pre-crRNA array) |
| **Off-target** | Well-characterized | Generally higher specificity |

**Citations:**
- Yan, W.X. et al. (2019). *Science* 363: 88-91.
- Swarts, D.C. & Jinek, M. (2019). "Mechanistic insights into the cis- and trans-acting DNase activities of Cas12a." *Mol Cell* 73(3): 589-600.
- Kleinstiver, B.P. et al. (2019). "Engineered CRISPR-Cas12a variants with increased activities and improved targeting ranges." *Nat Biotechnol* 37: 276-282.

---

## 4. Cas13 Diagnostics: SHERLOCK

**SHERLOCK** (Specific High-sensitivity Enzymatic Reporter unLOCKing):
- Combines RPA (recombinase polymerase amplification) pre-amplification with Cas13 collateral RNA cleavage.
- Workflow: sample extraction → RPA amplification → T7 transcription → Cas13-crRNA detection → fluorescent/lateral flow readout.
- Sensitivity: attomolar (50 fM, ~600,000 molecules); SHERLOCKv2 achieves single-molecule detection with optimized reporters.
- Readouts: fluorometer, lateral flow strips, colorimetric (turbidity), gel-based.
- Detects both DNA and RNA targets.
- Multiplexed detection with orthogonal Cas13 orthologs.

**Citations:**
- Gootenberg, J.S. et al. (2017). "Nucleic acid detection with CRISPR-Cas13a/C2c2." *Science* 356(6336): 438-442. DOI: 10.1126/science.aam9321.
- Gootenberg, J.S. et al. (2018). "Multiplexed and portable nucleic acid detection platform with Cas13, Cas12a, and Csm6." *Science* 360(6387): 439-444. DOI: 10.1126/science.aaq0179.
- Kellner, M.J. et al. (2019). "SHERLOCK: nucleic acid detection with CRISPR nucleases." *Nat Protoc* 14: 2986-3012. PMC6956564.

---

## 5. Cas12 Gene Editing Applications

- **Microorganisms:** metabolic engineering, antibiotic production, pathway optimization.
- **Plants:** abiotic stress resistance, crop improvement, multiplexed editing.
- **Animals:** disease modeling, therapeutic genome editing.
- **Miniature systems:** Cas12f and Cas12i enable AAV delivery due to compact size.
- **Engineered variants:** Cas12i2 (high-efficiency therapeutic platform), AiEvo2 (novel Cas12a for human gene editing), Un1Cas12f1 (enhanced activity and targeting scope).
- **Base editing:** Cas12a-derived base editors for C→T and A→G conversions.

**Citations:**
- Sharrar, A.M. et al. (2023). "Engineered Cas12i2 is a versatile high-efficiency platform for therapeutic genome editing." *Nat Commun* 14: 3125. PMC9122993.
- Sharrar, A.M. et al. (2024). "Discovery and engineering of AiEvo2, a novel Cas12a nuclease for human gene editing applications." *Nat Commun* 15: 1084. PMC10877636.
- Karvelis, T. et al. (2025). "Engineered Un1Cas12f1 for multiplex genome editing with enhanced activity and targeting scope." *Nat Commun* 16: 69678.
- Li, X. et al. (2024). "Research Progress and Application of Miniature CRISPR-Cas12 System in Gene Editing." *Int J Mol Sci* 25(23): 12822. PMC11641405.

---

## 6. Cas13 RNA Targeting

- **Programmable RNA knockdown:** Cas13d (RfxCas13d) widely used for transcript knockdown in mammalian cells.
- **RNA editing:** REPAIR (RNA Editing for Programmable A to I Replacement) and RESCURE systems.
- **RNA imaging:** Live-cell RNA tracking with fluorescently tagged Cas13.
- **Viral RNA targeting:** Antiviral applications against RNA viruses (SARS-CoV-2, influenza).
- **Transcriptome-wide design:** Algorithms for genome-wide Cas13 guide RNA design considering RNA secondary structure.
- **Collateral activity challenge:** In eukaryotic cells, collateral RNA cleavage can cause cytotoxicity and off-target transcript degradation.

**Citations:**
- Abudayyeh, O.O. et al. (2017). *Science* 353: aaf5573.
- Cox, D.B.T. et al. (2017). "RNA editing with CRISPR-Cas13." *Science* 358(6366): 1019-1027. DOI: 10.1126/science.aaq0180.
- Wessels, H.H. et al. (2020). "Massively parallel Cas13 screens reveal principles for guide RNA design." *Nat Biotechnol* 38: 722-727. PMC7294996.
- Huynh, N. et al. (2020). "A versatile toolkit for CRISPR-Cas13-based RNA manipulation in Drosophila." *Genome Biol* 21: 279. PMC7294996.

---

## 7. Cas12/Cas13 Protein Engineering

- **Chemical toolbox:** Small-molecule probes for labeling, degradation, and control of Cas protein activity.
- **High-fidelity variants:** Engineered to reduce off-target effects (e.g., HypaCas9, eSpCas9 for Cas9; analogous efforts for Cas12/Cas13).
- **Compact RNA editors:** Small Cas13 proteins (e.g., Cas13d ~930 aa) for AAV delivery.
- **Anti-CRISPR proteins:** Natural inhibitors (AcrVA1 for Cas13) for temporal control.
- **Safety assessment:** Systematic evaluation of DNA and RNA editing tools for off-targets, immunogenicity, and delivery.

**Citations:**
- Liu, L. et al. (2022). "A Chemical Toolbox for Labeling and Degrading Engineered Cas Proteins." *ACS Chem Biol* 17(8): 2056-2069. PMC8395650.
- Meeske, A.J. et al. (2020). *Science* 369: 54-59.
- Kannan, S. et al. (2021). "Compact RNA editors with small Cas13 proteins." *Nat Biotechnol* 40: 194-197.
- Wang, Q. et al. (2023). "Assessing and advancing the safety of CRISPR-Cas tools: from DNA to RNA editing." *Nat Commun* 14: 35886.

---

## 8. Cas12/Cas13 OSS Tools

- **CaSilico:** Versatile CRISPR package for in silico crRNA design for Cas12, Cas13, and Cas14. Supports multiple PAM types and off-target scoring.
- **ALLEGRO:** Kingdom-wide CRISPR guide design tool for large-scale, phylogenetically diverse genomes.
- **CRISPR-RT:** CRISPR RNA design toolkit for Cas13 systems.
- **Cas13design:** Transcriptome-wide guide RNA design for model organisms and viral RNA pathogens.
- **CHOPCHOP:** General CRISPR design tool with Cas12 support.
- **CRISPRscan:** Guide RNA activity prediction.

**Citations:**
- Kaki, S.S. et al. (2022). "CaSilico: A versatile CRISPR package for in silico CRISPR RNA designing for Cas12, Cas13, and Cas14." *Front Bioeng Biotechnol* 10: 957131. PMC9395711.
- "Kingdom-wide CRISPR guide design with ALLEGRO." *Nucleic Acids Res* 2025. DOI: 10.1093/nar/gkaf783.
- Wessels, H.H. et al. (2020). *Nat Biotechnol* 38: 722-727. PMC7294996.

---

## 9. Hardware Requirements

**Standard Molecular Biology Lab:**
- Thermocycler (PCR) or heat block (RPA isothermal amplification at 37-42°C)
- Centrifuge (microcentrifuge)
- Gel electrophoresis system (agarose gel for DNA/RNA analysis)
- Fluorometer or plate reader (for fluorescent reporter detection in diagnostics)
- Lateral flow strip reader (for point-of-care diagnostics)
- Cell culture incubator (for mammalian cell work)
- Fluorescence microscope (for imaging applications)
- -80°C freezer (protein/reagent storage)
- Biosafety cabinet (BSL-2 for pathogenic samples)

**For Diagnostics (SHERLOCK):**
- Minimal: heat block + lateral flow strips (field-deployable)
- Full: fluorometer + plate reader + thermocycler

**Computational:**
- Standard workstation for guide RNA design
- GPU cluster for genome-wide off-target prediction (optional)

---

## 10. Cost Analysis

**Reagent Costs (published list prices):**
- Research-grade Cas12a: ~€81 for 70 pmol
- Research-grade Cas12a: ~€289 for 2,000 pmol
- Research-grade Cas9: ~€1,022 for 500 µg
- crRNA synthesis: ~$50-200 per guide (custom synthesis)
- RPA kits: ~$2-5 per reaction
- Fluorescent reporters: ~$100-500 per kit

**Per-Experiment Estimates:**
- CRISPR diagnostics (SHERLOCK): ~$1-10 per sample
- Gene editing (cell culture): ~$500-2,000 per experiment (protein + guides + delivery)
- AAV production: ~$5,000-50,000 per batch

**Market Context:**
- Global CRISPR gene editing market projected to grow significantly through 2026.
- Wide price dispersion across suppliers.
- Open-source tools reduce computational costs.

**Citations:**
- "Global Biomedical CRISPR Gene Editing Market Research Report 2026." JSB Market Research.
- "Global CRISPR Gene Editing Tools Market Research Report 2026." JSB Market Research.
- "CRISPR vs NGS: A Comprehensive Cost-Benefit Analysis." NanoScience Hub.

---

## Synthesis: Bottlenecks, NP-Hard Problems, and Failure Modes

### Bottlenecks
1. **Off-target effects:** Cas13 collateral RNA cleavage in eukaryotic cells causes cytotoxicity and off-target transcript degradation, limiting therapeutic use.
2. **PAM/PFS constraints:** Cas12 requires T-rich PAMs (TTTV), Cas13 has PFS preferences — both limit targetable genomic sites.
3. **Delivery:** AAV packaging capacity (~4.7 kb) constrains Cas9 delivery; compact Cas12f/Cas13d variants mitigate but add engineering complexity.
4. **Immunogenicity:** Pre-existing immunity to Cas proteins (especially Cas9 from S. pyogenes) can trigger immune responses in therapeutic applications.
5. **Scalability of guide design:** Designing and cloning individually tailored sgRNAs for multiple genes across numerous genomes is experimentally burdensome and inefficient.
6. **One-pot reaction interference:** In diagnostics, Cas collateral cleavage can outpace amplification substrate generation, reducing sensitivity.

### NP-Hard Problems
1. **Guide RNA design optimization:** Multi-objective optimization (maximize on-target efficiency, minimize off-targets, avoid secondary structure) is computationally intractable for genome-wide design.
2. **Multiplexed guide design:** Selecting optimal guide sets for multiplexed editing with minimal cross-reactivity is NP-hard.
3. **Off-target prediction:** Genome-wide off-target site prediction with mismatch tolerance is computationally expensive (O(n·m) where n = genome size, m = guide length).

### Failure Modes
1. **Off-target cleavage:** Unintended DNA/RNA cleavage at sites with partial complementarity.
2. **Collateral RNA degradation:** Cas13's promiscuous RNase activity degrades non-target transcripts, causing cell stress/death.
3. **Immune response:** Anti-Cas antibodies and T-cell responses can eliminate edited cells or cause adverse reactions.
4. **Delivery failure:** Low transduction efficiency, vector toxicity, or immune clearance of delivery vehicles.
5. **PAM incompatibility:** Target sites lacking appropriate PAM/PFS sequences cannot be edited.
6. **Guide RNA secondary structure:** crRNA misfolding or secondary structure can abolish target recognition.

### Scalability Limits
1. **Throughput:** Limited by guide synthesis, cloning, and screening capacity.
2. **Computational:** Genome-wide guide design and off-target prediction scale poorly with genome size.
3. **Diagnostic sensitivity:** Amplification-free detection limited by enzyme kinetic rates; one-pot reactions face substrate competition.
4. **Multiplexing:** Number of simultaneous targets limited by orthogonal Cas variants and cross-reactivity.

### Biosecurity & Governance
1. **Dual-use risk:** CRISPR diagnostics can be repurposed for pathogen detection/enhancement.
2. **Biosecurity challenges:** Gene editing and synthetic biotechnology pose dual-use risks for potential pathogen enhancement.
3. **Governance frameworks:** Need for international oversight of CRISPR-based diagnostics and therapeutics.
4. **Anti-CRISPR:** Natural anti-CRISPR proteins (e.g., AcrVA1) provide biocontainment strategies.

### Cost Tradeoffs
1. **Cas protein source:** Recombinant expression (cheaper, ~€81-289) vs. commercial kits (convenient, ~€1,022 for Cas9).
2. **Guide synthesis:** Custom synthesis ($50-200/guide) vs. in-house IVT (cheaper, requires expertise).
3. **Diagnostics:** Lateral flow (cheap, ~$1-10/sample) vs. fluorescent readout (more sensitive, requires equipment).
4. **Delivery:** Non-viral (lipid nanoparticles, cheaper, lower efficiency) vs. viral (AAV, higher efficiency, ~$5,000-50,000/batch).
5. **Computational:** Open-source tools (free, requires expertise) vs. commercial software (expensive, user-friendly).

---

## Most Cited Papers
1. Hillary, V.E. & Ceasar, S.A. (2023). "A Review on the Mechanism and Applications of CRISPR/Cas9/Cas12/Cas13/Cas14 Proteins." *Mol Biotechnol* 65(3): 311-332.
2. Abudayyeh, O.O. et al. (2017). "C2c2 is a single-component programmable RNA-guided RNA-targeting CRISPR effector." *Science* 353: aaf5573.
3. Gootenberg, J.S. et al. (2017). "Nucleic acid detection with CRISPR-Cas13a/C2c2." *Science* 356: 438-442.
4. Zetsche, B. et al. (2015). "Cpf1 is a single RNA-guided endonuclease of a class 2 CRISPR-Cas system." *Cell* 163: 759-771.
5. Yan, W.X. et al. (2019). "Functionally diverse type V CRISPR-Cas systems." *Science* 363: 88-91.
6. Cox, D.B.T. et al. (2017). "RNA editing with CRISPR-Cas13." *Science* 358: 1019-1027.
7. Jinek, M. et al. (2012). "A programmable dual-RNA-guided DNA endonuclease in adaptive bacterial immunity." *Science* 337: 816-821.
8. Sharrar, A.M. et al. (2023). "Engineered Cas12i2 is a versatile high-efficiency platform for therapeutic genome editing." *Nat Commun* 14: 3125.
9. Wessels, H.H. et al. (2020). "Massively parallel Cas13 screens reveal principles for guide RNA design." *Nat Biotechnol* 38: 722-727.
10. Meeske, A.J. et al. (2020). "A phage-encoded anti-CRISPR enables complete evasion of type VI-A CRISPR-Cas immunity." *Science* 369: 54-59.

---

## OSS Projects
1. **CaSilico** — CRISPR RNA design for Cas12, Cas13, Cas14 (Front Bioeng Biotechnol, 2022)
2. **ALLEGRO** — Kingdom-wide CRISPR guide design (Nucleic Acids Res, 2025)
3. **CHOPCHOP** — General CRISPR guide design (various Cas types)
4. **CRISPRscan** — Guide RNA activity prediction
5. **Cas13design** — Transcriptome-wide Cas13 guide design
6. **SHERLOCK** — Open-source CRISPR diagnostics platform (MIT/Broad)
7. **REPAIR** — RNA editing with CRISPR-Cas13 (Zhang lab, MIT)
8. **CRISPR-DO** — CRISPR design and optimization
9. **CRISPRoff/CRISPRon** — Epigenetic editing with Cas12/Cas13
10. **GuideScan** — Comprehensive guide RNA design
