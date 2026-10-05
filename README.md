# 🧬 Genetic Engineering Platform

Unified platform for genetic engineering: CRISPR design, protein engineering, synthetic biology, gene therapy, computational genomics, metabolic engineering, single-cell genomics, epigenomics, AI/ML, and biosecurity.

## Architecture

### System Overview

```mermaid
graph TB
    subgraph Input["Input Layer"]
        DNA[DNA/RNA Sequences]
        PROT[Protein Sequences]
        OMICS[Omics Data]
    end

    subgraph Core["Core Processing Layer"]
        CRISPR[CRISPR Design<br/>Cas9/Cas12a/Cas13<br/>Base/Prime Editing]
        PROTEIN[Protein Engineering<br/>Structure/Stability]
        SYN[Synthetic Biology<br/>Circuits/Pathways]
        GEN[Genomics<br/>Variants/Assembly]
        GT[Gene Therapy<br/>Vectors/Delivery]
        MET[Metabolic Eng<br/>FBA/Strain Opt]
        AIML[AI/ML<br/>Protein LMs<br/>Variant Effect]
    end

    subgraph Integration["Integration Layer"]
        KG[Knowledge Graph<br/>SPARQL/GraphML]
        EB[EventBus<br/>Pub/Sub]
        DT[Digital Twin<br/>Simulation]
        PIPE[Pipeline<br/>Compose/Async]
    end

    subgraph Security["Biosecurity Layer"]
        SCREEN[Sequence Screening<br/>Threat Patterns]
        BSL[BSL Classification<br/>1-4 Clearance]
        AUDIT[Audit Trail<br/>Logging]
        WM[Watermarking<br/>Provenance]
    end

    subgraph Output["Output Layer"]
        DESIGN[Designs]
        PRED[Predictions]
        REPORT[Reports]
        ALERT[Alerts]
    end

    DNA --> CRISPR
    DNA --> GEN
    PROT --> PROTEIN
    OMICS --> AIML
    DNA --> SYN
    DNA --> GT
    OMICS --> MET

    CRISPR --> KG
    PROTEIN --> KG
    GEN --> KG
    SYN --> EB
    GT --> EB
    MET --> DT

    KG --> SCREEN
    EB --> BSL
    DT --> AUDIT
    SCREEN --> WM

    SCREEN --> ALERT
    BSL --> ALERT
    KG --> REPORT
    DT --> REPORT
    CRISPR --> DESIGN
    PROTEIN --> PRED
    GEN --> PRED
```

### Data Flow

```mermaid
sequenceDiagram
    participant U as User
    participant P as Pipeline
    participant C as CRISPR
    participant B as Biosecurity
    participant KG as KnowledgeGraph
    participant DT as DigitalTwin

    U->>P: Run workflow
    P->>C: Design gRNA
    C-->>P: gRNA + efficiency
    P->>B: Screen sequence
    B-->>P: Risk assessment
    alt Passes screening
        P->>KG: Store design
        P->>DT: Simulate effect
        DT-->>P: Predicted outcome
        P-->>U: Results
    else Fails screening
        B-->>U: Alert + reason
    end
```

### NP-Hard Problem Map

```mermaid
graph LR
    subgraph NP-Hard["NP-Hard Problems"]
        PF[Protein Folding<br/>Unger & Moult 1993]
        PD[Protein Design<br/>Pierce & Winfree 2002]
        GA[Genome Assembly<br/>Medvedev 2007]
        MSA[Multiple Sequence Alignment<br/>Wang & Jiang 1994]
        HA[Haplotype Assembly<br/>MEC Formulation]
        MPO[Metabolic Pathway Opt<br/>MILP]
        GCD[Gene Circuit Design<br/>Combinatorial]
        PTD[Phylogenetic Tree<br/>Reconstruction]
        RNA[RNA Inverse Folding]
    end

    subgraph Solvers["Our Solvers"]
        PF --> ESM[ESM/AlphaFold<br/>Embedding-based]
        PD --> KMER[k-mer LM<br/>Scoring]
        GA --> GREEDY[Greedy Assembly<br/>Overlap Graph]
        MSA --> PROG[Progressive<br/>Alignment]
        HA --> PAR[Partitioning<br/>Heuristic]
        MPO --> LP[scipy.linprog<br/>LP Relaxation]
        GCD --> BFS[BFS<br/>Path Finding]
        PTD --> NJ[Neighbor-Joining<br/>Approximation]
        RNA --> DYN[Dynamic Programming<br/>Approximation]
    end
```

### Multi-Agent Coordination

```mermaid
sequenceDiagram
    participant CEO as CEO/Director
    participant ORCH as Orchestrator
    participant CL as Cluster Leader
    participant W as Worker Agent

    CEO->>ORCH: Strategic goal
    ORCH->>CL: Decompose into clusters
    CL->>W: Assign specialized tasks
    W->>W: Execute (TDD)
    W->>CL: Return results
    CL->>ORCH: Aggregate cluster output
    ORCH->>CEO: Synthesize + decide
    CEO->>ORCH: Next wave / refine
```

### Digital Twin Feedback Loop

```mermaid
graph LR
    subgraph Sim["Digital Twin Simulation"]
        S1[Cell Count] --> S2[Temperature]
        S2 --> S3[pH]
        S3 --> S4[Metabolites]
        S4 --> S1
    end

    subgraph Real["Real World"]
        R1[Experiment] --> R2[Measurement]
        R2 --> R3[Analysis]
    end

    Sim -->|Predict| Real
    Real -->|Calibrate| Sim
```

## Archify Macro Architecture

See [`docs/archify-macro-architecture.html`](docs/archify-macro-architecture.html) for the full Archify-generated macro architecture diagram.

## Code Wiki

See [`docs/code-wiki/`](docs/code-wiki/) for the auto-generated code wiki with Mermaid diagrams for all modules.

## Quick Start

```bash
# Install
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Run examples
python examples/basic_usage.py

# Docker
docker-compose up -d
```

## Modules

| Module | Description | Key Algorithms |
|--------|-------------|----------------|
| `crispr` | Guide RNA design, off-target prediction | Rule Set 2, CFD scoring, Cas9/Cas12a/Cas13, Base/Prime Editing |
| `protein` | Protein sequence analysis, design | Stability prediction, pI calculation, secondary structure |
| `genomics` | Variant calling, assembly, phasing | Pileup calling, greedy assembly, chromosome-aware phasing |
| `synbio` | Genetic circuit design, pathway optimization | Logic gates, flux optimization, MoClo, RBS, promoters, terminators |
| `genetherapy` | Vector design, delivery optimization | Titer estimation, immunogenicity, MOI, dose optimization |
| `metabolic` | FBA, strain optimization | Greedy LP, FVA, GPR rules, robustness analysis, flux sampling |
| `aiml` | Protein LMs, variant effect, DTI | k-mer embeddings, cosine similarity, model registry, caching |
| `biosecurity` | Sequence screening, compliance | Risk scoring, dual-use detection, BSL classification, watermarking |
| `integration` | Knowledge graph, event bus, digital twin | SPARQL, GraphML, shortest path, connected components |
| `pipeline` | Multi-step workflow composition | Chaining, async, parallel, conditional, retry, metrics |
| `sizing` | Tier recommendations, cost/timeline estimates | Lab/startup/pharma profiles, serialization |

## Research Foundation

Built on 100-agent research across 10 clusters:
- CRISPR-Cas Systems (Cas9, Cas12, Cas13, base/prime editing)
- Protein Engineering (de novo design, structure prediction, stability)
- Synthetic Biology (genetic circuits, pathways, DNA synthesis)
- Gene Therapy (AAV, lentivirus, delivery, immune response)
- Computational Genomics (variants, assembly, haplotypes, MSA)
- Metabolic Engineering (FBA, strain optimization, GEMs)
- Single-Cell Genomics (scRNA-seq, spatial, multi-omics)
- Epigenomics (methylation, histones, chromatin, 3D genome)
- AI/ML for Genomics (protein LMs, variant effect, DTI, GFMs)
- Integrated Systems (KG, event buses, multi-agent, digital twins)

## NP-Hard Problems Addressed

- Protein folding (Unger & Moult 1993)
- Protein design (Pierce & Winfree 2002)
- Genome assembly (Medvedev 2007)
- Multiple sequence alignment (Wang & Jiang 1994)
- Haplotype assembly (MEC formulation)
- Metabolic pathway optimization (MILP)
- Gene circuit design (combinatorial)
- Phylogenetic tree reconstruction
- RNA inverse folding

## Tests

1114 tests passing across 11 modules. All modules follow TDD (test-first, red-green-refactor).

## License

MIT
