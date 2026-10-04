# Cluster 10: Knowledge Graphs for Genetic Engineering

## Overview

Knowledge graphs (KGs) are graph-structured data models that represent entities as nodes and relationships as edges, typically stored as RDF triples (subject–predicate–object) or labeled property graphs. In genetic engineering, KGs integrate heterogeneous biological data—genes, proteins, diseases, drugs, pathways, variants—into a unified queryable framework enabling inference, discovery, and machine learning at scale.

---

## 1. State-of-the-Art Approaches

### 1.1 Biomedical Knowledge Graphs for Genetic Engineering

| KG / Tool | Description | Scale | Citation |
|-----------|-------------|-------|----------|
| **VariantKG** | Scalable tool for analyzing human genomic variants using KGs and graph ML. Extracts variant-level genetic info, annotates with metadata, converts to RDF. | COVID-19 patient variants | Prasanna et al., 2025 (PMC11790625) |
| **Mantis-ML 2.0 / BIKG** | AstraZeneca's Biological Insights Knowledge Graph integrated with GNNs for phenome-wide gene-disease target identification. | 8.7M edges, 17,197 genes (BIKG subgraph); 146M+ edges total | PMC11078195 |
| **AIMedGraph** | Multi-relational KG for genes, genetic alterations, therapeutic and clinical impacts. Curates disease-drug-gene-variant relationships. | 15,367 genes from DisGeNET | Quan et al., 2023 (PMC9976745) |
| **GenomicKB** | Consolidates genomic databases, experimental studies, literature, and public repositories into unified KG. | Multi-source | Feng et al., 2023 |
| **Hetionet** | Open-source biomedical KG integrating 29 public databases for drug repurposing via metapath analysis. | 47,031 nodes (11 types), 2.25M edges (24 types) | bioinformatics reference |

### 1.2 KG Construction Pipelines

- **Top-down**: Define ontology first, then extract knowledge aligned to it (W3C standards).
- **Bottom-up**: Mine existing data/literature for patterns and relationships.
- **Hybrid**: LLM-based extraction (KGGen) with iterative entity clustering to reduce sparsity.
- **Five-step ecological/biomedical pipeline**: (1) Identify data requirements, (2) Develop ontology, (3) ETL to graph DB, (4) Embed for ML, (5) Downstream modeling.

### 1.3 Graph ML Integration

- **Graph Neural Networks (GCNs)**: Propagate features to neighboring nodes; used in Mantis-ML 2.0 achieving AUC 0.88 for gene-disease prediction.
- **Graph embeddings**: Node2Vec, TransE compress graphs into machine-learnable representations.
- **Link prediction**: Triple classification for novel hypothesis generation.

---

## 2. NP-Hard Problems in Knowledge Graphs

### 2.1 Query Answering Complexity

| Problem | Complexity | Source |
|---------|-----------|--------|
| **Basic Graph Pattern (BGP) matching** | NP-complete (reduction from 3-colourability) | Krötzsch, 2024 (TU Dresden Lecture 7) |
| **SPARQL query answering** | NP-hard (reduction from SAT); actually harder (QBF evaluation) | Krötzsch, 2018 (Lecture 8) |
| **QBF evaluation** | PSPACE-complete; NP-hard and coNP-hard | Krötzsch, 2018 |

### 2.2 Implications for Genetic Engineering KGs

- Multi-hop retrieval over biomedical KGs (e.g., UMLS: 407K nodes, 3.4M edges; PubMedKG: 54.4M nodes, 86.5M edges) faces exponential growth in reachable entities with hop depth.
- A 2-hop expansion from a high-degree UMLS concept (~33K 1-hop neighbors) can involve >10⁹ reachable edges.
- SPARQL query answering over large KGs is fundamentally intractable for complex patterns; heuristic and approximate methods are necessary.

---

## 3. Algorithms

### 3.1 Traversal Algorithms

| Algorithm | Complexity | Use Case |
|-----------|-----------|----------|
| **BFS** | O(V + E) | k-hop neighborhood expansion; context bloat around hubs |
| **DFS** | O(V + E) | Path enumeration, cycle detection, topological sort |
| **Bidirectional search** | O(b^(d/2)) | Entity-to-entity queries; halves exponent vs unidirectional |
| **Beam search** | O(b·k) | Semantic-guided expansion using embedding similarity |

### 3.2 Ranking Algorithms

| Algorithm | Complexity | Use Case |
|-----------|-----------|----------|
| **PageRank** | O(k·(V+E)) | Global entity importance; static prior |
| **Personalized PageRank (PPR)** | O(1/(ε·α)) local push | Query-relative relevance; primary GraphRAG signal |
| **Betweenness centrality** | O(V·E) | Bridge/broker identification |

### 3.3 GraphRAG Pipeline

1. Documents → Entity/Relation extraction → Knowledge Graph
2. User query → Entity linking (anchor nodes)
3. Graph algorithms (traversal / PPR / centrality / community)
4. Relevant subgraph → Linearize to text → LLM context → Answer

### 3.4 Embedding & Scalability Algorithms

- **SEPAL** (Scalable Embedding Propagation Algorithm): Subdivides KG into bounded subgraphs for GPU-efficient embedding; multiple-fold decreased train times with bounded memory.
- **NodePiece / EARL**: Embed subset of entities, train encoder for the rest to reduce GPU memory pressure.
- **LogosKG**: Hardware-aligned framework with degree-aware partitioning, cross-graph routing, on-demand caching; O(|E| log |E| + |T|) complexity.

---

## 4. Open-Source Tools

### 4.1 KG Construction & Management

| Tool | Architecture | License | Stars/Funding |
|------|-------------|---------|---------------|
| **Neo4j** | Property graph, Cypher | GPLv3 / Commercial | Industry standard |
| **Cognee** | Graph-first AI memory, Dreamify tuning | Apache 2.0 | Local-first friendly |
| **Nexarag** | Modular KG platform for research, Neo4j-backed, MCP-compatible | Open-source | JOSS 2025 |
| **Understand-Anything** | Codebase → interactive KG, multi-agent interoperability | Open-source | Egonex |
| **Mem0** | Vector-first + optional graph (Mem0g) | Apache 2.0 | 41K stars, $24M raised |
| **Zep / Graphiti** | Temporal knowledge graph, Neo4j-based | Apache 2.0 | 24K+ stars |
| **Letta (ex-MemGPT)** | OS-style tiered memory | Apache 2.0 | $10M seed |
| **Supermemory** | Atomic memory units + graph + MCP | Apache 2.0 | Google exec backed |

### 4.2 Graph Analytics Libraries

| Library | Device | Matrix-based | Scalability | Path Reconstruction |
|---------|--------|-------------|-------------|---------------------|
| **GraphBLAS** | CPU | ✓ | ✗ | ✗ |
| **cuGraph (RAPIDS)** | GPU | ✓ | ✗ | ✓ |
| **DGL** | GPU | ✗ | ✓ | ✗ |
| **PyG** | GPU | ✗ | ✓ | ✗ |
| **igraph / NetworkX / graph-tool** | CPU | ✗ | ✗ | ✓ |
| **LogosKG** | CPU/GPU | ✓ | ✓ | ✓ |

### 4.3 Domain-Specific KGs

- **KBpedia**: Integrates OpenCyc, UMBEL, GeoNames, DBpedia, Wikipedia, Wikidata; includes Biosecurity reference concept.
- **Hetionet**: 29 public databases, drug repurposing focus.
- **Gene Ontology (GO)**: Three sub-ontologies (Molecular Function ~12K terms, Biological Process ~30K, Cellular Component ~4.5K), DAG structure.

---

## 5. Hardware Requirements

### 5.1 Large-Scale KG Retrieval (LogosKG)

| Component | Specification |
|-----------|--------------|
| CPU | Dual AMD EPYC 9454 48-Core (192 threads) |
| RAM | 256 GB |
| GPU | 2× NVIDIA H100 NVL (94 GB VRAM each) |
| OS | Ubuntu 22.04 (HIPAA-compliant) |

### 5.2 Memory Footprints of Biomedical KGs

| KG | Nodes | Edges | Memory |
|----|-------|-------|--------|
| UMLS | 407K | 3.4M | 1.5 GB |
| PubMedKG | 54.4M | 86.5M | 23.5 GB |

### 5.3 Consumer/Prosumer Hardware

- **NVIDIA DGX Spark**: 128 GB unified memory, ArangoDB + Ollama or Neo4j + Ollama stack.
- **NVIDIA DGX Station**: Large HBM + Grace DRAM, supports vLLM with 49B+ models.
- **Minimum for LLM-based triple extraction**: Sufficient memory for chosen LLM (8B–49B+).

### 5.4 Scalability Constraints

- Billion-edge graphs cannot be loaded entirely into memory; require degree-aware partitioning and on-demand caching.
- 2-hop expansion from high-degree nodes can consume tens of GB for adjacency materialization.
- GPU memory limits require subgraph-based embedding (SEPAL approach).

---

## 6. Cost Analysis

### 6.1 KG Creation Costs (Paulheim, ISWC 2018)

| Method | Cost per Triple | Total Dev Cost |
|--------|-----------------|----------------|
| **Manual curation** | $2–$6 | — |
| **Automatic extraction** | $0.01–$0.15 (15–250× cheaper) | — |
| **DBpedia** | — | $5.1M (4.9M + 2.2M LOC) |
| **YAGO** | — | $1.6M (1.6M LOC incl. WordNet) |

### 6.2 Enterprise KG Costs

- **Pilot-to-production**: $10–20M, 5–15 person team (Graph Praxis).
- **Market**: $6.9B at 27% production adoption.
- **Ontology tax**: Ongoing schema maintenance cost that outpaces value delivered.

### 6.3 Cost-Quality Tradeoff

- Manual curation yields highest semantic validity but at $2–$6/triple.
- Automatic extraction is 15–250× cheaper but quality varies.
- Cost per triple correlates with semantic validity—should be an evaluation metric.

---

## 7. Scalability Limits

### 7.1 Fundamental Limits

| Limit | Description | Source |
|-------|-------------|--------|
| **Exponential traversal growth** | Reachable entities grow exponentially with hop depth | LogosKG (arXiv 2604.18913) |
| **Memory wall** | Billion-edge graphs exceed single-device RAM | LogosKG |
| **GPU memory** | Embedding models cannot fit largest graphs in GPU memory | SEPAL (arXiv 2507.00965) |
| **Query complexity** | SPARQL BGP matching is NP-complete | Krötzsch |

### 7.2 Mitigation Strategies

- **Degree-aware partitioning**: Divide KG into balanced subgraphs processed independently.
- **On-demand caching**: Load only required subgraphs; keep rest on disk.
- **Matrix-based representation**: Replace pointer-based structures with sparse matrix ops for vectorized computation.
- **Local push PPR**: O(1/(ε·α)) independent of graph size.
- **Subgraph embedding (SEPAL)**: Bounded-size subgraphs that fit in GPU memory.

### 7.3 Empirical Scalability

- LogosKG achieves deterministic accuracy on billion-edge graphs on single-device hardware.
- SEPAL shows multiple-fold decreased train times and bounded memory usage across 7 KGs and 46 downstream tables.
- Larger KGs bring value: suboptimal embedding of larger KG may outperform high-quality embedding of smaller KG.

---

## 8. Biosecurity Governance

### 8.1 Dual-Use Risks

| Threat | Description | Source |
|--------|-------------|--------|
| **GenAI-generated synthetic proteins/toxins** | GenAI lowers barrier to misuse in biosciences | arXiv 2510.15975v2 |
| **Jailbreak attacks** | Safety guardrails circumvented via deceptive prompts | 130 expert interviews |
| **Autonomous AI agents** | Dual-use challenges from autonomous biotech agents | 74% of experts call for new governance |

### 8.2 KG-Specific Biosecurity

- **KBpedia Biosecurity RC**: Structured biosecurity concept mapped to OpenCyc, UMBEL, Wikidata, Wikipedia.
- **Ecological KG for H5N1**: KG approach to track highly pathogenic avian influenza across species.
- **Data filtering**: Rigorous input filtering to block harmful sequence/pathway queries.
- **Real-time monitoring**: Block harmful requests at inference time.

### 8.3 Governance Recommendations

- Multi-layered defense: data filtering + ethical alignment + real-time monitoring.
- Secure-by-design technologies embedded throughout GenAI lifecycle.
- Adaptive governance frameworks for AI in biosciences.

---

## 9. Failure Modes

### 9.1 Three Tiers of Enterprise KG Failure (Atlan/Improvado 2026)

| Tier | Failure Pattern | Root Cause |
|------|----------------|------------|
| **Organizational** | No clear owner, wrong scope, weak sponsorship | Built as research project, not operational capability |
| **Technical** | Ontology drift, schema rigidity, entity resolution failure | Not fed from live, governed metadata source |
| **Economic** | Ontology tax, cost blowout, skills gap | People cost outpaces value delivered |

### 9.2 Key Failure Modes

| Failure Mode | Description | Evidence |
|-------------|-------------|----------|
| **Ontology drift** | Schema diverges from real-world entities as source systems change; no re-validation trigger | Graph Praxis |
| **Entity resolution failure** | Different identifiers for same entity (e.g., TP53 = P53_HUMAN = 7157 = ENSG00000141510) not merged → confidently wrong answers | Children's Medical Center Dallas |
| **Schema rigidity** | Inability to accommodate new data types without major redesign | 19-practitioner interview study |
| **Siloed graphs** | Multiple disconnected KGs with no interoperability | Enterprise KG deployments |
| **Pilot-to-production stall** | <15% of enterprise KG projects move past pilot | Improvado 2026 |

### 9.3 KG Quality Dimensions

- **Completeness**: Systematic literature review of 56 articles (Issa et al., 2021, cited 133×).
- **Accuracy, timeliness, provenance, accessibility**: Additional quality dimensions.
- **Common challenges**: Difficulty querying, poor data quality, evolving provenance, schema inconsistencies, lack of organizational standardization.

---

## 10. Ontologies

### 10.1 Ontology vs. Knowledge Graph

| Aspect | Ontology | Knowledge Graph |
|--------|----------|-----------------|
| **Role** | Schema layer | Instance layer |
| **Content** | Entity types, relationships, rules | Actual nodes, edges, properties |
| **Size** | Few hundred–few thousand classes | Hundreds of millions of nodes |
| **Language** | OWL, RDFS, SHACL | RDF, Cypher, property graphs |
| **Example** | Gene Ontology (GO) | Wikidata (100M+ entities, 1.5B+ statements) |

### 10.2 Key Biological Ontologies

| Ontology | Domain | Structure | Terms |
|----------|--------|-----------|-------|
| **Gene Ontology (GO)** | Gene/protein function | DAG (multiple parents) | ~46,500 total |
| — Molecular Function | Biochemical activity | DAG | ~12,000 |
| — Biological Process | Biological objectives | DAG | ~30,000 |
| — Cellular Component | Subcellular location | DAG | ~4,500 |
| **Disease Ontology (DO)** | Human diseases | DAG | — |
| **Human Phenotype Ontology (HPO)** | Clinical phenotypes | DAG | — |
| **OBO Foundry** | Biomedical ontologies | DAG | — |

### 10.3 Ontology Construction Challenges

- **Schema mapping**: Aligning data models across source databases (e.g., UniProt IDs vs. Entrez Gene IDs vs. Ensembl IDs).
- **Entity resolution**: Mapping identifiers to canonical nodes (e.g., TP53 → P53_HUMAN → 7157 → ENSG00000141510).
- **DAG vs. tree**: Biological terms have multiple parents (e.g., "glucose transport" is both "carbohydrate transport" and "sugar import").
- **Borrow before building**: Reuse Schema.org, FOAF, SKOS, BFO, Gene Ontology, FIBO.

### 10.4 Ontologically Grounded KGs

- Reification of abstract objects for language-agnostic representation.
- Separation of static conceptual information from dynamic factual data.
- Conceptualism and conceptual realism (Cocchiarella 2001) for KG integration.

---

## 11. Bottlenecks Summary

1. **Computational complexity**: SPARQL BGP matching is NP-complete; multi-hop retrieval scales exponentially.
2. **Memory constraints**: Billion-edge graphs exceed single-device RAM; GPU memory limits embedding models.
3. **Entity resolution**: Mapping heterogeneous identifiers to canonical nodes is the most underestimated step.
4. **Ontology drift**: Schema diverges from real-world entities without re-validation triggers.
5. **Cost**: Manual curation $2–$6/triple; enterprise deployments $10–20M with 5–15 person teams.
6. **Pilot-to-production gap**: <15% of enterprise KG projects move beyond pilot.
7. **Data quality**: Poor data quality, schema inconsistencies, and lack of standardization recur across deployments.
8. **Biosecurity**: GenAI lowers barrier to misuse; KGs must incorporate governance and filtering.

---

## 12. Most Cited Papers

1. **Issa et al. (2021)** — "Knowledge Graph Completeness: A Systematic Literature Review" — cited 133× (IEEE)
2. **Paulheim (2018)** — "How much is a Triple? Estimating the Cost of Knowledge Graph Creation" — ISWC
3. **Krötzsch (2024)** — "Knowledge Graphs: Expressive Power and Complexity of SPARQL" — TU Dresden
4. **Prasanna et al. (2025)** — "VariantKG: A scalable tool for analyzing genomic variants using KGs and GML" — PMC
5. **Quan et al. (2023)** — "AIMedGraph: A comprehensive multi-relational KG" — cited 26×
6. **SEPAL (2025)** — "Scalable Feature Learning on Huge Knowledge Graphs" — arXiv 2507.00965
7. **LogosKG (2025/2026)** — "Hardware-Optimized Scalable and Interpretable KG Retrieval" — arXiv 2604.18913
8. **KGGen (2025)** — "Extracting Knowledge Graphs from Plain Text with Language Models" — arXiv 2502.09956
9. **Nexarag (2025)** — "Democratizing Reproducible KG Contexts for LLM Research" — JOSS
10. **Generative AI for Biosciences (2025)** — "Emerging Threats and Roadmap to Biosecurity" — arXiv 2510.15975v2

---

## 13. References

- Prasanna S, Kumar A, Rao D, Simoes EJ, Rao P. "A scalable tool for analyzing genomic variants of humans using knowledge graphs and graph machine learning." PMC11790625, 2025.
- "Phenome-wide identification of therapeutic genetic targets, leveraging knowledge graphs, graph neural networks, and UK Biobank data." PMC11078195.
- Quan X et al. "AIMedGraph: a comprehensive multi-relational knowledge graph." PMC9976745, 2023.
- Krötzsch M. "Knowledge Graphs: Expressive Power and Complexity of SPARQL." TU Dresden Lectures 7–8, 2018/2024.
- Paulheim H. "How much is a Triple? Estimating the Cost of Knowledge Graph Creation." ISWC 2018.
- Issa S et al. "Knowledge Graph Completeness: A Systematic Literature Review." IEEE, 2021.
- "LogosKG: Hardware-Optimized Scalable and Interpretable Knowledge Graph Retrieval." arXiv 2604.18913 / PMC12870703, 2025/2026.
- "SEPAL: Scalable Feature Learning on Huge Knowledge Graphs for Downstream Machine Learning." arXiv 2507.00965, 2025.
- "KGGen: Extracting Knowledge Graphs from Plain Text with Language Models." arXiv 2502.09956, 2025.
- "Nexarag: Democratizing Reproducible Knowledge Graph Contexts for LLM Research." JOSS, 2025.
- "Generative AI for Biosciences: Emerging Threats and Roadmap to Biosecurity." arXiv 2510.15975v2, 2025.
- "Understanding ecological systems using knowledge graphs: an application to highly pathogenic avian influenza." BioAdvances, 2025.
- "Enterprise Knowledge Graph Pitfalls: Why Projects Fail." Atlan, 2026.
- "Knowledge Graphs in Practice: Characterizing their Users, Challenges, and Visualization Opportunities." arXiv 2304.01311v4.
- "Towards Ontologically Grounded and Language-Agnostic Knowledge Graphs." IWCS 2023.
- "Biomedical Knowledge Graphs and Ontologies." Bioinformatics reference.
- "Open-Source Memory Layers for AI Agents: The Complete 2026 Comparison." TheGenios, 2026.
- NVIDIA dgx-spark-playbooks: txt2kg. GitHub.
