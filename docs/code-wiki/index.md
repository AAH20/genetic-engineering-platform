# Code Wiki — Genetic Engineering Platform

Auto-generated module documentation with Mermaid diagrams.

## Module Index

### CRISPR Design (`src/crispr/`)

```mermaid
graph TD
    subgraph CRISPR["CRISPR Module"]
        V[validate_grna_sequence] --> D[design_grna]
        D --> E[calculate_efficiency_score]
        E --> O[find_off_target_sites]
        O --> K[find_off_target_sites_indexed]
        K --> B[find_off_target_sites_both_strands]
        D --> C12a[design_grna_cas12a]
        D --> C13[design_grna_cas13]
        D --> BE[design_base_editor_grna]
        D --> PE[design_prime_editing_grna]
        D --> PG[design_paired_grna]
        D --> BG[design_grna_batch]
        D --> CV[design_grna_for_variant]
    end
```

**Key Functions:**
- `design_grna(target, pam, min_efficiency, max_off_targets)` — Main gRNA design
- `design_grna_cas12a(target, pam)` — Cas12a (Cpf1) with TTTV PAM
- `design_grna_cas13(target, pfs)` — Cas13 RNA-targeting with PFS
- `design_base_editor_grna(target, editor_type)` — CBE/ABE base editing
- `design_prime_editing_grna(target, pam)` — pegRNA for prime editing
- `design_paired_grna(target, pam)` — Paired gRNAs for deletions
- `design_grna_batch(targets, pam)` — Batch design for multiple targets
- `design_grna_for_variant(target, variant)` — Cas9 variant support
- `find_off_target_sites_indexed(grna, genome)` — K-mer indexed search
- `find_off_target_sites_both_strands(grna, genome)` — Both-strand search
- `_pam_matches_iupac(potential, pattern)` — IUPAC ambiguity codes

---

### Protein Engineering (`src/protein/`)

```mermaid
graph TD
    subgraph Protein["Protein Module"]
        PS[ProteinSequence] --> MW[calculate_molecular_weight]
        PS --> PI[calculate_isoelectric_point]
        PS --> ST[predict_stability]
        PS --> SS[predict_structure]
        PS --> SEC[predict_secondary_structure]
        PS --> DOM[identify_domains]
        PS --> SP[predict_signal_peptide]
        PS --> CH[calculate_charge_at_ph]
    end
```

**Key Functions:**
- `ProteinSequence(sequence)` — Dataclass with properties
- `calculate_molecular_weight(seq)` — MW in Daltons
- `calculate_isoelectric_point(seq)` — Estimated pI
- `predict_stability(seq)` — Stability score [0,1]
- `predict_structure(seq)` — alpha/beta/mixed
- `predict_secondary_structure(seq)` — helix/sheet/coil fractions
- `identify_domains(seq)` — Hydrophobic domain detection
- `predict_signal_peptide(seq)` — N-terminal signal peptide
- `calculate_charge_at_ph(seq, ph)` — Net charge at pH

---

### Genomics (`src/genomics/`)

```mermaid
graph TD
    subgraph Genomics["Genomics Module"]
        CV[call_variants] --> FV[filter_variants_by_vaf]
        CV --> FQ[filter_variants_by_quality]
        CV --> FT[filter_variants_by_type]
        CV --> IN[call_indels]
        CV --> SV[call_structural_variants]
        CV --> PH[phase_variants]
        PH --> PHC[phase_variants_by_chromosome]
        PHC --> HD[calculate_haplotype_diversity]
        CV --> ASM[assemble_contigs]
        ASM --> N50[calculate_n50]
        CV --> VCF[to_vcf]
        CV --> FASTA[write_fasta / read_fasta]
    end
```

**Key Functions:**
- `call_variants(reference, reads)` — SNV calling
- `call_indels(reference, reads)` — Indel detection
- `call_structural_variants(reference, reads)` — SV detection
- `phase_variants(variants, reads)` — Haplotype phasing
- `phase_variants_by_chromosome(variants, reads)` — Chromosome-aware
- `assemble_contigs(reads, min_overlap)` — Greedy assembly
- `to_vcf(variants, reference_name)` — VCF export
- `write_fasta(sequences, filepath)` — FASTA I/O
- `filter_variants_by_vaf(variants, min_vaf)` — VAF filtering

---

### Synthetic Biology (`src/synbio/`)

```mermaid
graph TD
    subgraph SynBio["Synthetic Biology Module"]
        GC[GeneticCircuit] --> LG[LogicGate]
        GC --> EV[evaluate]
        GC --> VAL[validate]
        GC --> LOG[CircuitLogger]
        PO[PathwayOptimizer] --> OP[optimize_pathway]
        PO --> CY[calculate_yield]
        DN[DNASynthesis] --> OH[design_overhangs]
        DN --> MC[design_moclo_overhangs]
        DN --> RBS[calculate_rbs_strength]
        DN --> PR[predict_promoter_strength]
        DN --> TE[predict_terminator_efficiency]
        DN --> CO[optimize_codon_usage]
    end
```

**Key Functions:**
- `GeneticCircuit(name, inputs, outputs)` — Logic gate circuits
- `PathwayOptimizer(model)` — Pathway optimization
- `DNASynthesis` — DNA synthesis design
- `design_moclo_overhangs(parts)` — MoClo assembly
- `calculate_rbs_strength(seq)` — RBS calculator
- `design_rbs(seq, host)` — RBS designer
- `predict_promoter_strength(seq)` — Promoter strength
- `design_promoter(host)` — Promoter designer
- `predict_terminator_efficiency(seq)` — Terminator efficiency
- `design_terminator(host)` — Terminator designer
- `optimize_codon_usage(seq, host)` — Codon optimization
- `calculate_cai(seq, host)` — Codon Adaptation Index

---

### Gene Therapy (`src/genetherapy/`)

```mermaid
graph TD
    subgraph GeneTherapy["Gene Therapy Module"]
        V[Vector] --> CC[check_capacity]
        V --> TIT[calculate_titer]
        V --> OPT[optimize_titer]
        V --> CVT[compare_vector_types]
        V --> IR[predict_immunogenicity]
        V --> TE[predict_transduction_efficiency]
        V --> OD[optimize_delivery]
        V --> DOSE[calculate_dose]
        V --> MOI[calculate_moi]
        V --> TEFF[calculate_transduction_efficiency]
        V --> VOL[calculate_required_volume]
        V --> OD2[optimize_dose]
        V --> COST[calculate_treatment_cost]
        V --> CS[predict_capsid_stability]
        V --> AB[predict_capsid_antibody_binding]
        V --> IE[suggest_immune_evasion]
        V --> TA[analyze_transgene_sequence]
        V --> IRISK[calculate_immunogenicity_risk]
        V --> GB[write_genbank / read_genbank]
    end
```

**Key Functions:**
- `Vector(name, capacity, serotype)` — Viral vector dataclass
- `calculate_titer(vector_type, transgene_size, purity)` — Titer estimation
- `optimize_titer(transgene_size, purity)` — Best vector selection
- `predict_immunogenicity(serotype, age, prior_exposure)` — Immune response
- `predict_transduction_efficiency(serotype, tissue)` — Transduction
- `optimize_delivery(tissue, vector_type, age)` — Delivery route
- `calculate_dose(weight, tissue, vector_type)` — Dose calculation
- `calculate_moi(dose, cell_count)` — Multiplicity of infection
- `calculate_transduction_efficiency(moi)` — Poisson-based
- `optimize_dose(weight, tissue, vector_type, target_efficiency)` — Dose opt
- `analyze_transgene_sequence(seq)` — PolyA, splice sites, GC
- `predict_capsid_stability(serotype)` — Capsid stability
- `suggest_immune_evasion(serotype, age)` — Evasion strategies

---

### Metabolic Engineering (`src/metabolic/`)

```mermaid
graph TD
    subgraph Metabolic["Metabolic Module"]
        MM[MetabolicModel] --> AR[add_reaction]
        MM --> SO[set_objective]
        MM --> SF[solve_fba]
        MM --> FVA[fva]
        MM --> RF[robustness_analysis]
        MM --> SP[shadow_prices]
        MM --> GPR[add_gpr_rule]
        MM --> KG[knockout_gene]
        MM --> ER[add_exchange_reaction]
        MM --> SFS[sample_flux_space]
        MM --> GFR[get_flux_range]
        PD[PathwayDesigner] --> DP[design_pathway]
        PD --> CPY[calculate_pathway_yield]
        SO2[StrainOptimizer] --> OK[optimize_knockouts]
        SO2 --> SK[simulate_knockout]
        SO2 --> CK[compare_knockouts]
    end
```

**Key Functions:**
- `MetabolicModel()` — FBA model with reactions
- `solve_fba()` — Greedy LP approximation
- `fva(fraction_of_optimum)` — Flux Variability Analysis
- `robustness_analysis(reaction_name)` — Robustness to perturbation
- `shadow_prices()` — Dual variables for metabolites
- `add_gpr_rule(reaction_name, rule)` — Gene-Protein-Reaction rules
- `knockout_gene(gene)` — Gene knockout simulation
- `add_exchange_reaction(name, metabolite)` — Nutrient uptake/secretion
- `sample_flux_space(n_samples, seed)` — Hit-and-run sampling
- `PathwayDesigner(model)` — Pathway design via BFS
- `StrainOptimizer(model)` — Knockout optimization

---

### AI/ML (`src/aiml/`)

```mermaid
graph TD
    subgraph AIML["AI/ML Module"]
        PLM[ProteinLanguageModel] --> EMB[embed]
        PLM --> EMBB[embed_batch]
        PLM --> EMBC[embed_cached]
        PLM --> PVE[predict_variant_effect]
        PLM --> PVEB[predict_variant_effect_batch]
        PLM --> PPA[predict_pathogenicity]
        PLM --> PPAB[predict_pathogenicity_batch]
        PLM --> CCS[calculate_conservation_score]
        PLM --> PBA[predict_binding_affinity]
        PLM --> PSEL[predict_selectivity]
        PLM --> GS[generate_sequence]
        PLM --> CS[cosine_similarity]
        PLM --> FS[find_similar]
        PLM --> SAVE[save / load]
        PLM --> CC[clear_cache]
        PLM --> GCS[get_cache_stats]
        MR[ModelRegistry] --> REG[register]
        MR --> GET[get]
        MR --> LM[list_models]
        MR --> RM[remove]
    end
```

**Key Functions:**
- `ProteinLanguageModel(name)` — k-mer bag-of-words model
- `embed(sequence)` — Embedding vector
- `embed_batch(sequences)` — Batch embedding
- `embed_cached(sequence)` — Cached embedding
- `predict_variant_effect(wt, mut, pos)` — Variant effect score
- `predict_pathogenicity(seq, pos, ref, alt)` — Pathogenicity
- `cosine_similarity(seq1, seq2)` — Embedding similarity
- `find_similar(query, candidates, top_k)` — Top-k similar
- `save(path)` / `load(path)` — Model persistence
- `ModelRegistry` — Model registry

---

### Biosecurity (`src/biosecurity/`)

```mermaid
graph TD
    subgraph Biosecurity["Biosecurity Module"]
        SS[SequenceScreener] --> SCR[screen_sequence]
        SS --> SB[screen_batch]
        SS --> CRS[calculate_risk_score]
        SS --> CRB[calculate_risk_batch]
        SS --> CH[check_homology]
        SS --> CHB[check_homology_both_strands]
        SS --> BCH[batch_check_homology]
        DUD[DualUseDetector] --> DUD2[detect_dual_use]
        DUD --> CRL[classify_risk_level]
        CC[ComplianceChecker] --> CHK[check_compliance]
        CC --> GR[generate_report]
        BG[BiosecurityGate] --> EVAL[evaluate]
        BG --> AL[audit_log]
        BG --> CB[add_callback]
        BG --> BSL[classify_bsl_level]
        BG --> CHC[check_bsl_clearance]
        BG --> WM[embed_watermark]
        BG --> VW[verify_watermark]
        BG --> LCP[load_custom_patterns]
        BG --> SPF[save_patterns_to_file]
    end
```

**Key Functions:**
- `SequenceScreener()` — Threat pattern screening
- `screen_sequence(seq)` — Both-strand screening
- `screen_batch(sequences)` — Batch screening
- `calculate_risk_score(seq)` — Risk score [0,1]
- `check_homology(seq, ref)` — K-mer Jaccard
- `check_homology_both_strands(seq, ref)` — Both-strand
- `DualUseDetector()` — Dual-use detection
- `ComplianceChecker()` — Regulatory compliance
- `BiosecurityGate()` — Full gate evaluation
- `classify_bsl_level(seq)` — BSL 1-4 classification
- `check_bsl_clearance(seq, user_level)` — Clearance check
- `embed_watermark(seq, watermark)` — DNA watermarking
- `load_custom_patterns(patterns)` — Configurable patterns

---

### Integration (`src/integration/`)

```mermaid
graph TD
    subgraph Integration["Integration Module"]
        KG[KnowledgeGraph] --> AE[add_entity]
        KG --> AR[add_relation]
        KG --> Q[query]
        KG --> QSP[query_sparql]
        KG --> GN[get_neighbors]
        KG --> SP[shortest_path]
        KG --> GCC[get_connected_components]
        KG --> GDC[get_degree_centrality]
        KG --> TG[to_graphml]
        KG --> TCJ[to_cytoscape_json]
        KG --> TD[to_dict / from_dict]
        KG --> TJ[to_json / from_json]
        KG --> AWO[annotate_with_ontology]
        KG --> QBO[query_by_ontology]
        ONT[Ontology] --> LO[load_ontology]
        ONT --> GT[get_term]
        ONT --> GP[get_parents]
        EB[EventBus] --> PUB[publish]
        EB --> SUB[subscribe]
        EB --> GE[get_events]
        DT[DigitalTwin] --> US[update_state]
        DT --> GS2[get_state]
        DT --> SIM[simulate]
        CFG[Config] --> LF[load_from_file]
        CFG --> SF[save_to_file]
        CFG --> G[get]
        CFG --> S[set]
    end
```

**Key Functions:**
- `KnowledgeGraph()` — Entity-relation graph
- `add_entity(id, type, properties)` — Add entity
- `add_relation(src, rel, tgt, weight)` — Add relation
- `query(type, properties)` — Indexed query
- `query_sparql(query)` — SPARQL-like queries
- `shortest_path(src, tgt)` — BFS shortest path
- `get_connected_components()` — Component detection
- `get_degree_centrality()` — Centrality scores
- `to_graphml()` — GraphML export
- `to_cytoscape_json()` — Cytoscape JSON
- `to_dict()` / `from_dict()` — Serialization
- `Ontology()` — SO/GO/ChEBI terms
- `EventBus()` — Pub/sub event bus
- `DigitalTwin(id)` — Simulation twin
- `Config()` — Configuration system

---

### Pipeline (`src/pipeline/`)

```mermaid
graph TD
    subgraph Pipeline["Pipeline Module"]
        P[Pipeline] --> AS[add_step]
        P --> APS[add_parallel_step]
        P --> ACS[add_conditional_step]
        P --> R[run]
        P --> RA[run_async]
        P --> RCOE[run_continue_on_error]
        P --> C[compose]
        P --> SP[split]
        P --> CL[clone]
        P --> IS[insert_step]
        P --> RS[remove_step]
        P --> RS2[replace_step]
        P --> GS[get_step]
        P --> GM[get_metrics]
        P --> RM[reset_metrics]
        P --> TD[to_dict / from_dict]
        P --> TJ[to_json / from_json]
        PS[PipelineStep] --> EX[execute]
        PS --> RC[retry_count]
        PS --> RD[retry_delay]
        APS2[AsyncPipelineStep] --> AEX[execute]
        PS2[ParallelStep] --> PEX[execute]
        PS3[ConditionalStep] --> CEX[execute]
    end
```

**Key Functions:**
- `Pipeline(name, description)` — Composable pipeline
- `add_step(step)` — Add processing step
- `add_parallel_step(steps)` — Concurrent execution
- `add_conditional_step(predicate, if_true, if_false)` — Branching
- `run(initial_value, context)` — Execute pipeline
- `run_async(initial_value, context)` — Async execution
- `run_continue_on_error(initial_value, context)` — Error tolerance
- `compose(other)` — Pipeline composition
- `split(step_name)` — Split at step
- `clone()` — Deep copy
- `insert_step(step, index)` — Dynamic insertion
- `remove_step(name)` — Dynamic removal
- `get_metrics()` — Observability
- `PipelineStep(name, func)` — Step with retry
- `AsyncPipelineStep(name, func)` — Async step
- `ParallelStep(steps)` — Parallel execution
- `ConditionalStep(predicate, if_true, if_false)` — Branching

---

### Sizing (`src/sizing/`)

```mermaid
graph TD
    subgraph Sizing["Sizing Module"]
        RT[recommend_tier] --> SR[SizingRecommendation]
        RT --> RTE[recommend_tier_with_explanation]
        RT --> RAT[recommend_all_tiers]
        SR --> EC[estimate_cost]
        SR --> ET[estimate_timeline]
        SR --> CT[compare_tiers]
        SR --> GTC[get_tier_capabilities]
        OG[OnboardingGuide] --> TD2[to_dict]
        OG --> TJ2[to_json]
        OG --> FD[from_dict]
    end
```

**Key Functions:**
- `recommend_tier(team_size, budget, cores, storage)` — Tier recommendation
- `recommend_tier_with_explanation(...)` — With explanation
- `recommend_all_tiers(...)` — All tier recommendations
- `estimate_cost(tier, team_size, budget)` — Cost estimation
- `estimate_timeline(tier, team_size)` — Timeline in days
- `compare_tiers(tier1, tier2)` — Tier comparison
- `get_tier_capabilities(tier)` — Capability limits
- `OnboardingGuide(tier)` — Onboarding steps
- `to_dict()` / `to_json()` / `from_dict()` — Serialization

---

## Cross-Module Integration

```mermaid
graph LR
    CRISPR -->|gRNA| Biosecurity
    Protein -->|sequence| Integration
    Genomics -->|variants| Integration
    SynBio -->|circuits| Integration
    GeneTherapy -->|vectors| Integration
    Metabolic -->|flux| Integration
    AIML -->|predictions| Integration
    Integration -->|events| Pipeline
    Pipeline -->|orchestrates| CRISPR
    Pipeline -->|orchestrates| Protein
    Pipeline -->|orchestrates| Genomics
    Pipeline -->|orchestrates| SynBio
    Pipeline -->|orchestrates| GeneTherapy
    Pipeline -->|orchestrates| Metabolic
    Pipeline -->|orchestrates| AIML
```
