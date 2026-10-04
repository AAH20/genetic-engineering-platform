# Cluster 10: Ontologies for Genetic Engineering

## Topic
Ontologies for genetic engineering: Sequence Ontology (SO), Gene Ontology (GO), ChEBI, computational complexity, algorithms, open-source tools, hardware requirements, cost analysis, and scalability limits.

---

## 1. Ontologies in Genetic Engineering — Review

**Key finding:** Ontologies are critical infrastructure for genetic engineering, providing structured controlled vocabularies that enable automated reasoning, data integration, and cross-species comparison of gene function.

- **Alterovitz et al. (2010)** — "Ontology Engineering" (PMC4829499, cited 98×): Describes methods using information theory to automatically organize GO structure and optimize information distribution. GO and similar biomedical ontologies are crafted through painstaking manual processes.
- **Ontologies for Bioinformatics** (PMC2735951): Comprehensive review for molecular biologists. The Gene Ontology Consortium (GOC) formed alongside model organism genome mappings. GO is described as a "controlled vocabulary" with formal ontology characteristics: machine-readability, formal notation, hierarchical knowledge structure, relational associations. A global ontology paradigm is appropriate because there is a finite body of genetic information shared between all life on Earth.

---

## 2. Sequence Ontology (SO)

**Key finding:** SO provides standardized terms and relationships for describing biological sequence features, enabling automated reasoning over genomic annotations.

- **SO Project** (sequenceontology.org): Collaborative ontology for sequence feature annotation, initially developed by the Gene Ontology Consortium. Contributors include GMOD, WormBase, FlyBase, MGI, Sanger Institute, EBI. Part of the Open Biomedical Ontologies (OBO) library. Covers biological features (binding_site, exon), biomaterial features (aptamer, PCR_product), and experimental features.
- **Eilbeck et al. (2005)** — "The Sequence Ontology: a tool for the unification of genome annotations" (PMC1175956): SO began when FlyBase, WormBase, Ensembl, SGD, and MGI unified their annotation terms. SO is a directed acyclic graph (DAG) with three relationship types: `kind_of`, `derives_from`, `part_of`. SOFA (Sequence Ontology Feature Annotation) is a stabilized subset with 171 locatable sequence features. SO enables logical inference — software need only be aware of relationship types, not terms themselves.
- **Sequence Ontology Annotation Guide** (PMID 18629179): SO formally specifies sub-class, membership (mereological), and topological relationships. This provides the basis for an extensible object-oriented data model. Terms are defined with descriptive definitions agreed by the community.

---

## 3. Gene Ontology (GO)

**Key finding:** GO is the world's largest source of functional information on genes, with ~39,354 terms and 9.28M annotations across 5,495 species (Oct 2025 release).

- **GO Knowledgebase 2026** (PMC12807639): GO provides structured, computer-accessible representation of gene functions. Three aspects: Molecular Function (MF), Cellular Component (CC), Biological Process (BP). GO-CAMs (Causal Activity Models) combine multiple annotations into pathway models — 1,571 pathways as of July 2025, increased ~5× in 3 years. Three editions: `go-basic` (39,906 relations), `go` (78,889), `go-plus` (121,698, links to ChEBI, Uberon, Cell Ontology, SO, PATO, Protein Ontology).
- **GO Overview** (geneontology.org): GO is species-agnostic, organized as three disjoint DAGs. Terms connected via `is_a`, `part_of`, `has_part`, `regulates`, `negatively_regulates`, `positively_regulates`, `occurs_in`. GO is constantly revised by editors with broad biological knowledge. Multiple parentage allowed, reflecting non-linear biological realities.
- **Grokipedia — Gene Ontology**: GO originated in 1998 from FlyBase, MGD, and SGD. First formal description published in 2000 (Ashburner et al.). GO annotations use evidence codes (experimental, computational, literature). Over 1M experimentally supported annotations from 187,286 publications.

---

## 4. ChEBI (Chemical Entities of Biological Interest)

**Key finding:** ChEBI is a manually curated database and ontology of chemical entities, essential for describing small molecules in genetic engineering contexts.

- **ChEBI** (ebi.ac.uk/chebi): Open-access database of chemical entities — atoms, molecules, ions, radicals, complexes, conformers. >195,000 entries. Uses IUPAC and NC-IUBMB nomenclature. Provides ontological classification with parent/child relationships for chemical class and role queries. Macromolecules directly encoded by the genome (nucleic acids, proteins) are excluded.
- **About ChEBI**: Designated ELIXIR core data resource (2017) and Global core biodata resource (2022). Used by Rhea, MetaboLights, UniProt, GO, IEDB, Reactome, PubChem, BioModels, IntAct, SwissLipids. ChEBI is the sole source of accurate small molecule structural information linked to a stable identifier for many resources.
- **ChEBI in OLS** (ebi.ac.uk/ols4/ontologies/chebi): Version 255, CC BY 4.0 license. Part of OBO Foundry. Includes role ontology (1,648 role terms), subatomic particle classification (42 terms).

---

## 5. Ontologies and NP-Hard Problems

**Key finding:** Ontology-mediated querying is computationally hard — NP-complete for combined complexity even with simple query shapes.

- **Complexity of Contextuality** (arXiv 2506.09133): Finding the smallest ontological model is NP-hard. Deciding existence of a noncontextual ontological model of dimension k is at least exponential in the dimension of the theory. Computing the smallest noncontextual ontological model is inefficient in general.
- **OMQ with OWL 2 QL** (DOI 10.1145/3034786.3034791): Ontology-mediated query (OMQ) answering is NP-complete for combined complexity. Answering OMQs is already NP-hard for tree-shaped (acyclic) CQs, in contrast to LOGCFL-completeness of evaluating bounded treewidth CQs. No polynomial-time algorithm can construct FO-rewritings unless P = NP.
- **Dichotomies in Ontology-Mediated Querying** (arXiv 1804.06894): Studies complexity of ontology-mediated querying in the guarded fragment of first-order logic. Identifies fragments with PTime/coNP dichotomy. Almost all ontologies in BioPortal fall into these fragments. For other fragments, no such dichotomy exists (variation of Ladner's Theorem).

---

## 6. Ontology Algorithms and Reasoning

**Key finding:** High-performance description logic reasoners exist but face fundamental scalability challenges with large ontologies.

- **Tools Environment for Developing and Reasoning about Ontologies** (APSEC 2005, DOI 10.1109/APSEC.2005.21): Integrated tools environment for systematic development of OWL ontologies with transformation, reasoning assistance, and querying. Ensures consistency of shared ontologies in Semantic Web applications.
- **Oxford KRR Course** (cs.ox.ac.uk): Covers decidable fragments of first-order logic for knowledge representation, Datalog reasoning algorithms, description logics, ontology languages. Fundamental trade-off between representation power and computational properties.
- **Understanding and Improving Ontology Reasoning Efficiency** (ScienceDirect S0306437917306476): High-performance DL reasoners include FaCT++, HermiT, Konclude, Pellet, and TrOWL. Reasoning efficiency remains a bottleneck for large-scale ontologies.

---

## 7. Open-Source Ontology Tools

**Key finding:** A rich ecosystem of open-source ontology tools exists, from editors to reasoners to programmatic access libraries.

- **Awesome Ontology** (softono.com): Protégé (free, open-source ontology editor), VocBench (web-based collaborative OWL ontology management), NeOn Toolkit (open-source ontology engineering environment), OAK (Ontology Access Kit — Python library and CLI), OWLGrEd (UML-style graphical editor for OWL), Pellet 2 (open-source OWL DL reasoner for Java).
- **Open Ontologies** (arXiv 2605.09184): Open-source Rust-based system integrating OWL-RL reasoning, alignment, and lifecycle management into an LLM-orchestrated workflow via MCP. Single binary, no JVM. On OAEI Anatomy track: F1 = 0.832. Stable 1-to-1 matching is dominant factor in alignment quality. LLM with structured MCP tool access (F1 = 0.717) outperforms reading raw OWL (F1 = 0.323).
- **Open Ontologies Blog** (wonlab.top): Consistency checks drop from 4,936μs (HermiT) to 0.3μs (Open Ontologies Rust) — 16,000× faster. Three-layer architecture: Dynamics Layer (atomic operations + OWL-RL reasoning), Causal Layer (causal identification with PyWhy).

---

## 8. Hardware Requirements

**Key finding:** Ontology processing has significant hardware requirements, especially for reasoning and large-scale triple stores.

- **Memory Engines for Edge AI** (hostingersite.com): ESP32 (520KB SRAM) can only hold ~1,000 triples via flat file (20ms lookup) or ~2,500 triples via custom adjacency list (2ms lookup). Streaming approach supports unlimited size but 80-120ms per lookup. For devices with >512MB RAM, embedded triple stores with indexing provide best balance.
- **OntoCode Performance Sizing** (ontocode-vs.readthedocs.io): Hard limits: 10,000 ontology files per workspace, 50MB single file, 20M total RDF triples, 1M entities, 100K SQL/SPARQL result rows. Sizing tiers: Small (<100k triples, excellent), Medium (100k-5M, good), Large (5M-20M, pilot required), Extra-large (>20M, not supported).
- **OntoLogos Performance** (ontologos.readthedocs.io): RDFS engine runs until TBox rules saturate, sequential only. OWL RL engine supports parallelism (1-64 threads). RlEngine::new(n) affects ABox type-rule candidate expansion. Production integration requires ReasonerConfig::budget_secs for large DL corpora.

---

## 9. Cost Analysis

**Key finding:** Ontology development costs are dominated by human labor (schema design, construction, maintenance), but LLM automation is reducing costs by 40-60%.

- **ONTOCOM** (Springer LNCS 5554): Cost estimation model for ontology development projects, calibrated on 148 projects. Cost drivers: product-related (domain analysis complexity, conceptualization complexity), personnel-related (ontologist capability, expertise), project-related (automation support, decentralization). Prediction quality improved up to 50% with larger dataset.
- **GraphRAG Cost Cliff** (rebeauty-writing.com): Full GraphRAG indexing cost $33,000 for 5GB corpus (2024) → $33 (2025) via LazyGraphRAG (0.1% of original). KG-based RAG: $1,825/year vs vector RAG: $3,650/year (ArangoDB benchmark, 10K queries/day). Ontology tax justified at 5-10+ heterogeneous data sources. LLM automation reducing tax costs by 40-60%; governance is dominant remaining cost.
- **Cost Estimation with Ontology** (ScienceDirect S147466701532139X): Ontologies provide formalization for cost estimation in manufacturing. Cost Entity approach combines ABC method and cost accounting analysis. Ontology enables capitalization and formalization of cost-related knowledge.

---

## 10. Scalability Limits

**Key finding:** Ontology systems face fundamental scalability limits in materialization, reasoning, and evolution across hundreds of ontologies.

- **NCBO Resource Index** (Springer LNCS 17746-0_31): Knowledge base of 16.4 billion annotations linking 2.4M terms from 200 ontologies to 3.5M data elements. Population time reduced from 1 week to <1 hour through data distribution and ontology evolution optimization. Neither OntoDB nor DLDB could handle NCI Thesaurus (74,646 classes) — hours just for schema creation. Benchmarks obscure load-time costs for materialization.
- **OntoLearner** (arXiv 2607.01977): Modular Python library for ontology learning with LLMs. Releases 180 ontologies across 22 domains as machine-readable datasets on HuggingFace. NELL accumulated millions of beliefs but did not support invention of new classes. OLAF proposed fully automated pipeline for "minimum viable ontologies."
- **LLMs in Bio-Ontology Research** (PMC12649945): Creation and maintenance of biomedical ontologies remain highly challenging. Labor-intensive process creates critical gap: as biomedical knowledge grows exponentially, traditional ontology engineering cannot keep pace. GO and SO were built through years of iterative curation, consensus building, and peer review. Semi-automated text-mining and ML approaches require extensive feature engineering and expert validation.

---

## Bottlenecks

1. **Manual curation bottleneck**: GO and SO require years of expert-driven iterative curation, consensus building, and peer review. Traditional methods cannot keep pace with exponentially growing biomedical knowledge.
2. **Reasoning computational complexity**: OMQ answering is NP-complete for combined complexity; NP-hard even for tree-shaped CQs. Finding smallest ontological models is NP-hard.
3. **Materialization costs**: Large/deep ontologies (500K+ classes) have prohibitive load-time costs for materialization. Benchmarks often obscure these costs.
4. **Scalability limits**: Existing systems (OntoDB, DLDB) cannot handle NCI Thesaurus scale (74,646 classes). Resource Index requires 16.4B annotations across 200 ontologies.
5. **Human labor costs**: Ontology development dominated by human labor for schema design, construction, and maintenance. Governance is the dominant remaining cost even with LLM automation.
6. **Ontology evolution**: Ontologies are not stagnant — managing knowledge over time for evolving ontologies is a fundamental challenge.
7. **Extraction quality**: LLM-based triple extraction achieves only 0.52-0.73 F1 with local models, propagating errors in frequent rebuilds.

## Citations

1. Alterovitz G, et al. "Ontology Engineering." PMC4829499, 2010.
2. "Ontologies for Bioinformatics." PMC2735951.
3. Eilbeck K, et al. "The Sequence Ontology: a tool for the unification of genome annotations." PMC1175956, 2005.
4. "Sequence Ontology Annotation Guide." PMID 18629179.
5. "The Gene Ontology knowledgebase in 2026." PMC12807639.
6. Ashburner M, et al. "Gene Ontology: tool for the unification of biology." Nature Genetics, 2000.
7. Degtyarenko K, et al. "ChEBI: a database and ontology for chemical entities of biological interest." Nucleic Acids Res, 2008.
8. "Complexity of Contextuality." arXiv 2506.09133, 2025.
9. "The Complexity of Ontology-Based Data Access with OWL 2 QL." DOI 10.1145/3034786.3034791.
10. "Dichotomies in Ontology-Mediated Querying with the Guarded Fragment." arXiv 1804.06894, 2017.
11. Dong JS, et al. "A Tools Environment for Developing and Reasoning about Ontologies." APSEC 2005, DOI 10.1109/APSEC.2005.21.
12. "Understanding and improving ontology reasoning efficiency." Information Systems, ScienceDirect S0306437917306476.
13. "Open Ontologies: Tool-Augmented Ontology Engineering with Stable Matching Alignment." arXiv 2605.09184, 2026.
14. "ONTOCOM Revisited: Towards Accurate Cost Predictions for Ontology Development Projects." Springer LNCS 5554.
15. "The GraphRAG Cost Cliff: How $33,000 Became $33 in Eighteen Months." Rebeauty Atlas, 2025.
16. "NCBO Resource Index scalability." Springer LNCS 17746-0_31.
17. "OntoLearner: A Modular Python Library for Ontology Learning with Large Language Models." arXiv 2607.01977, 2026.
18. "Large Language Models in Bio-Ontology Research: A Review." PMC12649945.
19. "Memory Engines for Edge AI: Lightweight Ontology Stores on Microcontrollers." 2025.
20. "OntoCode Performance and Sizing." ontocode-vs.readthedocs.io.
21. "OntoLogos Performance and Scaling." ontologos.readthedocs.io.
