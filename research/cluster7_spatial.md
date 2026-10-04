# Cluster 7: Spatial Transcriptomics — Research Synthesis

## Overview

Spatial transcriptomics (ST) enables gene expression profiling while preserving spatial context within intact tissue sections. The field is broadly divided into two complementary technology families:

- **NGS-based (sequencing) methods**: Visium (10x), Stereo-seq (BGI), Slide-seq — unbiased whole-transcriptome capture on barcoded arrays, but limited spatial resolution (~55 µm for Visium, ~220 nm for Stereo-seq).
- **In situ imaging-based methods**: MERFISH, seqFISH+, Xenium (10x), CosMx (NanoString), MERSCOPE (Vizgen) — single-molecule sensitivity at subcellular resolution, but constrained to predesigned gene panels (hundreds to ~23,000 genes).

No current platform achieves both true single-cell resolution and unbiased whole-transcriptome coverage simultaneously.

---

## State-of-the-Art Approaches

### Platforms
| Platform | Type | Resolution | Capture Area | Cost (approx.) |
|----------|------|------------|--------------|----------------|
| 10x Visium | NGS | 55 µm spots | 6.5×6.5 mm | $3,293 + seq |
| 10x Visium HD | NGS | 2 µm | 6.5×6.5 mm | ~2× Stereo-seq |
| BGI Stereo-seq | NGS | ~220 nm (subcellular) | up to cm-scale | $3,837 + seq |
| 10x Xenium | Imaging | ~50 nm (subcellular) | 12×24 mm | ~$6,733 |
| NanoString CosMx | Imaging | ~50 nm (subcellular) | 20×15 mm | ~$6,325 |
| Vizgen MERSCOPE | Imaging | ~100 nm (subcellular) | 18×22 mm | ~$3,878 |
| Illumina StrataMap | NGS | single-cell | 7.5 cm² | TBD (2026) |

### Computational Methods
- **Cell-type deconvolution**: cell2location, RCTD, SPOTlight, Tangram, DestVI, SpiceMix, DSTG, FlashDeconv
- **Spatial domain identification**: BayesSpace, SpaGCN, STAGATE, GraphST, DeepST, SpaceFlow, CellCharter, Banksy, SPACEL, DUET, SPHENIC, TSstc
- **Cell-cell communication**: CellChat, CellPhoneDB, LIANA+, COMMOT, stLearn, NicheCompass
- **Spatially variable genes**: SpatialDE, Hotspot, SOMDE, SINFONIA, Maxspin
- **Gene imputation**: SpaOTsc, SpaGE, novoSpaRc, TANGRAM, stMCDI, stImpute
- **Registration/alignment**: PASTE/PASTE2 (Fused Gromov-Wasserstein OT), STalign (LDDMM), GPSA (GP warp), SPIRAL, INST-Align
- **Foundation models**: Geneformer, scGPT-spatial, Nicheformer, OmiCLIP, stFormer, DeepSpot

---

## Bottlenecks

1. **Resolution vs. breadth trade-off**: No platform achieves both single-cell/subcellular resolution AND unbiased whole-transcriptome coverage. NGS methods are transcriptome-wide but multi-cell per spot; imaging methods are single-cell but limited to gene panels.

2. **Lateral diffusion**: mRNA diffusion during capture blurs spatial signal in NGS-based methods, limiting effective resolution below the spot size.

3. **Optical crowding**: In imaging-based methods, high transcript density causes optical crowding, limiting multiplexing capacity and requiring complex sequential hybridization.

4. **Deconvolution accuracy**: Spot-based methods capture mixtures of cells per spot; deconvolution relies on scRNA-seq reference quality and introduces bias for rare cell types.

5. **Computational cost**: Deep learning methods for ST analysis require significant GPU resources (32GB+ VRAM for full fine-tuning of large models like Geneformer-316M).

6. **Tissue section integrity**: Physical sectioning introduces tears, warps, and non-isometric deformations that break registration algorithms.

7. **Scalability of imaging**: Imaging-based methods require 1–7 days of scanning time and specialized equipment, limiting throughput.

8. **Cost barriers**: Per-sample costs range from ~$3,000–$7,000+ (excluding sequencing), making large-scale studies prohibitively expensive.

9. **Cross-platform incompatibility**: Analysis pipelines are often incompatible across different ST technologies, hindering integrative analysis.

10. **3D reconstruction**: Registering serial sections for 3D reconstruction is an open problem; all incumbent method families (OT, diffeomorphic, GP warp) fail under tearing.

---

## NP-Hard Problems

1. **Optimal spatial domain detection**: Jointly clustering spots while respecting spatial contiguity constraints is computationally intractable for large datasets; most methods use approximations (HMRF, graph clustering, convex clustering).

2. **Cell-type deconvolution**: The deconvolution problem — estimating cell-type proportions from mixed spot profiles — is an underdetermined inverse problem; exact solutions require solving large-scale non-negative matrix factorization or Bayesian inference.

3. **Spatial transcript registration**: PASTE/PASTE2 cast registration as Fused Gromov-Wasserstein optimal transport, which is NP-hard in general; entropic regularization provides polynomial-time approximations.

4. **Cell-cell communication inference**: Reconstructing signaling networks from ligand-receptor co-expression with spatial constraints involves combinatorial optimization over cell neighborhoods.

5. **3D serial section alignment**: Non-rigid registration of serial sections with tears and non-isometric deformations is ill-posed; no exact algorithm exists for the general case.

6. **Gene imputation**: Spatially-aware gene imputation requires solving large-scale optimal transport or graph-based interpolation problems.

---

## Scalability Limits

- **Imaging throughput**: MERFISH/seqFISH+ require 1–7 days of imaging per sample; CosMx/MERSCOPE require 1–2 days. This limits cohort sizes.
- **Sequencing-based scaling**: Visium can process multiple sections per slide; Stereo-seq supports centimeter-scale capture areas; StrataMap (Illumina, 2026) offers 7.5 cm² capture with 22-hour sequencing.
- **Computational scaling**: Spacemake (Snakemake-based) enables parallel processing of multiple samples across technologies. Computational array reconstruction (Hu et al., 2025) eliminates imaging bottlenecks, scaling to 1.2 cm tissues (targeting 7 cm).
- **Data volume**: A single Visium run generates ~5000 spots × ~20,000 genes; Stereo-seq generates millions of subcellular locations. Storage and processing require HPC infrastructure.
- **Deep learning scaling**: Full fine-tuning of 1.4B-parameter models requires 32GB+ VRAM; PEFT methods (LoRA, gradient checkpointing) reduce this to 2–10GB.

---

## Hardware Requirements

- **NGS-based analysis**: Standard workstation (16–64 GB RAM, multi-core CPU) sufficient for most pipelines; GPU optional but recommended for deep learning methods.
- **Imaging-based analysis**: High-performance computing recommended; 16GB+ RAM minimum; NVIDIA GPU (A100/3090) recommended for training.
- **Foundation model fine-tuning**: Full fine-tuning of Geneformer-316M requires 32GB+ VRAM; PEFT (LoRA) reduces to 2.15GB peak VRAM; 1.4B-parameter UCE model requires 9.48GB with PEFT.
- **Storage**: 1–10 TB recommended for large-scale studies (raw images, spatial matrices, reference data).
- **Specialized equipment**: Imaging platforms require dedicated instruments (Xenium Analyzer, CosMx SMI, MERSCOPE); NGS platforms require standard sequencers (NovaSeq, NextSeq).

---

## Cost Trade-offs

| Platform | Library Cost | Sequencing | Total (approx.) | Resolution | Genes |
|----------|-------------|------------|-----------------|------------|-------|
| Visium | $3,293 | $500–1,500 | $3,800–4,800 | 55 µm | Whole transcriptome |
| Visium HD | ~$6,000 | $500–1,500 | $6,500–7,500 | 2 µm | Whole transcriptome |
| Stereo-seq | $3,837 | $500–1,500 | $4,300–5,300 | 220 nm | Whole transcriptome |
| Xenium | $6,733 | N/A | ~$6,733 | 50 nm | ~500 genes |
| CosMx | $6,325 | N/A | ~$6,325 | 50 nm | ~6,000 genes |
| MERSCOPE | $3,878 | N/A | ~$3,878 | 100 nm | ~1,000 genes |

**Key trade-offs**:
- NGS-based methods offer unbiased whole-transcriptome coverage but lower resolution.
- Imaging-based methods offer single-cell/subcellular resolution but limited gene panels and higher per-sample cost.
- Visium HD is ~2× more expensive than Stereo-seq for library construction despite analyzing fewer cells.
- Xenium is the most affordable imaging-based option.
- Sequencing costs add $500–$1,500 per sample for NGS-based methods.
- Computational costs (HPC, GPU) can add $1,000–$10,000+ per study depending on scale.

---

## Failure Modes

1. **Image misalignment**: Automated registration (e.g., Space Ranger) can misalign spots by microns, leading to gross misinterpretation of spatial patterns. Tissue folds, staining artifacts, and irregular geometry exacerbate this.

2. **Tissue warps and tears**: Physical sectioning introduces tears and warps that break spatial continuity. All incumbent registration methods (PASTE2, STalign, GPSA) collapse under severe tearing (error increases from ~722 px to ~855–931 px).

3. **Background noise**: Tissue-free spots, autofluorescence, and nonspecific binding create false signals. In CosMx/Xenium, channel leakage can mimic gene expression.

4. **Spot mixing**: In hypercellular regions (e.g., GBM), spot mixing inflates co-expression and generates false "hybrid" cell states.

5. **Segmentation errors**: In imaging-based methods, incorrect cell segmentation misassigns transcripts to wrong cells.

6. **Spatially patterned quality loss**: Near necrosis and hemorrhage, RNA quality degrades non-randomly. Naive QC filtering erases biologically relevant zones.

7. **Permeabilization artifacts**: Over- or under-permeabilization creates structured artifacts that mimic biological patterns.

8. **Deconvolution bias**: Reference-based deconvolution introduces bias for rare cell types and depends heavily on scRNA-seq reference quality.

9. **Cross-donor batch effects**: Deep ST models fail to generalize across donors due to expression distribution shifts; predictions regress to tissue centroid.

10. **Tear-collapse in 3D registration**: All three method families (OT, diffeomorphic, GP warp) converge to ~840–930 px error at severe tear, confirming a field-wide failure mode.

---

## Biosecurity Governance

Direct biosecurity literature for spatial transcriptomics is limited. Relevant considerations:

1. **Dual-use concerns**: ST could be used to map pathogen-host interactions in situ, including for enhanced pathogens. The same technology used to study COVID-19 pathogenesis could inform gain-of-function research.

2. **Data privacy**: Spatial transcriptomic data from human samples contains individual genetic information. Governance frameworks must address data sharing, consent, and re-identification risks.

3. **Environmental release**: ST is primarily an in vitro/in situ technique with low direct environmental risk, but sample handling and waste disposal require standard biosafety protocols.

4. **Synthetic biology intersection**: ST can validate spatial patterns of engineered gene circuits, raising governance questions about monitoring synthetic organism deployment.

5. **International coordination**: Platforms are commercially available from US (10x, NanoString, Vizgen, Illumina), China (BGI Stereo-seq), and Europe. Export controls and technology transfer policies may affect access.

6. **Standardization gap**: Lack of standardized protocols and reference materials complicates regulatory oversight and cross-laboratory validation.

---

## Most Cited Papers

1. Rao A, Barkley D, França GS, et al. "Exploring tissue architecture using spatial transcriptomics." *Nature*. 2021;596:211–220. (Seminal review)
2. Rodriques SG, Stickels RR, Goeva A, et al. "Slide-seq: a scalable technology for measuring genome-wide expression at high spatial resolution." *Science*. 2019;363:1463–1467.
3. Chen A, Liao S, Cheng M, et al. "Spatiotemporal transcriptomic atlas of mouse organogenesis using DNA nanoball-patterned arrays." *Cell*. 2022;185:1777–1792.
4. Maynard C, Collado-Torres L, Weber LM, et al. "Transcriptome-scale spatial gene expression in the human dorsolateral prefrontal cortex." *Nature Neuroscience*. 2021;24:425–436.
5. Ståhl PL, Salmén F, Vickovic S, et al. "Visualization and analysis of gene expression in tissue sections by spatial transcriptomics." *Science*. 2016;353:78–82. (Original ST method)
6. Tian L, Chen F, Macosko EZ. "The expanding vistas of spatial transcriptomics." *Nature Biotechnology*. 2023;41:773–782.
7. Littman R, Hemminger Z, Foreman R, et al. "Joint cell segmentation and cell type annotation for spatial transcriptomics." *Nature Methods*. 2024.
8. Hu C, et al. "Scalable spatial transcriptomics through computational array reconstruction." *Nature Biotechnology*. 2026;44:215–221.
9. Zhao E, Stone MR, Ren X, et al. "Spatial transcriptomics at subspot resolution with BayesSpace." *Nature Biotechnology*. 2021;39:1375–1384.
10. Longo SK, Guo MG, Ji AL, Khavari PA. "Integrating single-cell and spatial transcriptomics to elucidate intercellular tissue dynamics." *Nature Reviews Genetics*. 2021;22:627–644.

---

## Open Source Projects

| Project | Language | Description |
|---------|----------|-------------|
| squidpy | Python | Spatial single-cell analysis toolkit (scverse ecosystem) |
| Giotto | R/Python | Comprehensive spatial data analysis suite |
| STUtility | R | Visium data standardization, annotation, visualization |
| spacemake | Python/Snakemake | Modular, scalable ST pipeline for multiple technologies |
| MOSAIK | Python | End-to-end workflow for CosMx and Xenium data |
| PASTE/PASTE2 | Python | Probabilistic alignment of ST experiments |
| SPIRAL | R | Integrating and aligning ST data across experiments |
| Vitessce | JavaScript | Visual integration tool for spatial single-cell experiments |
| Voyager | R | Spatial transcriptomics visualization (Pachter lab) |
| BASS | R | Multiple sample analysis |
| SpaVAE | Python | Dimension reduction, clustering, batch integration, denoising |
| sopa | Python | Spatial omics processing and analysis |
| SpatialAgent | Python | Autonomous AI agent for spatial biology |
| ChatSpatial | Python | MCP server for ST analysis via natural language (60+ methods) |
| STAgent | Python | Autonomous multimodal LLM agent for end-to-end ST analysis |
| scvi-tools | Python | Probabilistic analysis of single-cell data |
| cell2location | Python | Cell-type deconvolution |
| Tangram | Python | scRNA-seq to ST mapping |
| BayesSpace | R | Bayesian spatial domain identification |
| SpaGCN | Python | Graph convolutional network for spatial clustering |
| GraphST | Python | Graph contrastive learning for ST clustering |
| STAGATE | Python | Topology-aware graph attention for spatial domains |
| DeepST | Python | Deep learning for spatial transcriptomics |
| CellCharter | Python | Cell neighborhood analysis |
| Banksy | Python | Clustering with spatial constraints |
| SpatialDE | Python | Spatially variable gene detection |
| Hotspot | Python | Spatial gene pattern detection |
| CellChat | R | Cell-cell communication inference |
| CellPhoneDB | Python | Ligand-receptor interaction analysis |
| LIANA+ | R/Python | Cell-cell communication benchmarking |
| COMMOT | Python | Cell-cell communication with spatial constraints |
| novoSpaRc | R | Spatial reconstruction from scRNA-seq |
| STalign | R | Diffeomorphic registration of ST data |
| SPACEL | Python | Spatial domain identification |
| MAEST | Python | Multi-sample spatial analysis |
| SpaGT | Python | Graph transformer for spatial transcriptomics |
| STAIG | Python | Image-aided graph contrastive learning for ST |
| DUET | Python | Convex clustering for spatial domain detection |
| SPHENIC | Python | Topology-aware multi-view clustering |
| TSstc | Python | Tailored spatial-scale modulation clustering |
| PASSAGE | Python | Phenotype-guided spatial clustering |
| Segger | Python | Cell segmentation for spatial data |
| Bering | Python | Cell segmentation and analysis |
| CellSAM | Python | Cell segmentation from images |
| FlashDeconv | Python | Fast cell deconvolution |
| SDePER | Python | Deep learning deconvolution |
| CLPLS | Python | Constrained least squares deconvolution |
| NODE | Python | Neural network deconvolution |
| DECLUST | Python | Deep clustering for ST |
| SCGP | Python | Spatial clustering with graph pooling |
| SR-DGN | Python | Spatial resolution deep graph network |
| AESTETIK | Python | Aesthetic spatial analysis |
| STAN | R | Spatial transcription factor analysis |
| SpaGRN | Python | Spatially aware GRN inference |
| scSpace | Python | Cell pseudo-space reconstruction |
| SOCS | Python | Trajectory inference in time-series ST |
| STORIES | Python | Spatial transcriptomics stories |
| eggplant | R | Common Coordinate Framework |
| Bento | Python | Subcellular analysis |
| SANTO | R | Coarse-to-fine alignment and stitching |
| SpaGFT | R | Graph Fourier transform for spatial omics |
| InSTAnT | R | Intracellular patterns of co-localisation |
| MuSpan | R | Multiscale analysis |
| DeepSpot | Python | ST prediction from H&E images |
| DeepSpot2Cell | Python | Virtual single-cell ST from H&E |
| InSituPy | Python | Histology-guided multi-sample analysis |
| MESA | R | Ecological inspired spatial analysis |
| SpatialQC | Python | Quality control for ST data |
| MerQuaCo | Python | Quality control for MERFISH |
| LazySlide | Python | Whole slide image analysis |
| pasta | R | Point pattern and lattice data analysis |
| rakaia | JavaScript | Scalable interactive visualization |
| semla | R | Spatially resolved transcriptomics analysis |
| sosta | Python | Spatial Omic Structure Analysis |
| SPATA2 | R | Spatial transcriptomics analysis toolkit |
| spatial-omics-tutorials | Python/R | Tutorials for spatial omics |
| scArches | Python | Transfer learning for scRNA-seq |
| PathML | Python | Computational pathology |
| CytoCommunity | Python | Tissue cellular neighborhoods |
| scCube | Python | Simulation of ST data |
| STUtility | R | Visium data analysis |
| STAgent | Python | Autonomous ST analysis agent |
| ChatSpatial | Python | MCP server for ST analysis |
| SpatialAgent | Python | AI agent for spatial biology |
| STAIG | Python | Image-aided graph contrastive learning |
| STalign | Python | Diffeomorphic registration |
| SPIRAL | R | ST data integration |
| PASTE2 | Python | Probabilistic alignment |
| INST-Align | Python | Implicit neural representation alignment |
| GPSA | Python | Gaussian process spatial alignment |
| CODA | Python | Diffeomorphic registration |
| Sutura | Python | Learned registration (contrastive) |
| TSstc | Python | Tailored spatial-scale clustering |
| SPHENIC | Python | Topology-aware clustering |
| DUET | Python | Convex clustering |
| PASSAGE | Python | Phenotype-guided clustering |
| STAGATE | Python | Graph attention clustering |
| GraphST | Python | Graph contrastive clustering |
| DeepST | Python | Deep learning clustering |
| SpaceFlow | Python | Spatial flow clustering |
| CellCharter | Python | Cell neighborhood clustering |
| Banksy | Python | Spatial clustering |
| SCGP | Python | Graph pooling clustering |
| SR-DGN | Python | Deep graph network clustering |
| AESTETIK | Python | Aesthetic clustering |
| MAEST | Python | Multi-sample clustering |
| SpaGT | Python | Graph transformer clustering |
| STAN | R | Transcription factor analysis |
| SpaGRN | Python | GRN inference |
| scSpace | Python | Pseudo-space reconstruction |
| SOCS | Python | Trajectory inference |
| STORIES | Python | ST analysis |
| eggplant | R | Common coordinate framework |
| Bento | Python | Subcellular analysis |
| SANTO | R | Alignment and stitching |
| SpaGFT | R | Graph Fourier transform |
| InSTAnT | R | Co-localisation analysis |
| MuSpan | R | Multiscale analysis |
| DeepSpot | Python | H&E prediction |
| DeepSpot2Cell | Python | Virtual single-cell ST |
| InSituPy | Python | Histology-guided analysis |
| MESA | R | Ecological analysis |
| SpatialQC | Python | Quality control |
| MerQuaCo | Python | MERFISH QC |
| LazySlide | Python | WSI analysis |
| pasta | R | Point pattern analysis |
| rakaia | JavaScript | Visualization |
| semla | R | ST analysis |
| sosta | Python | Spatial analysis |
| SPATA2 | R | ST analysis |
| spatial-omics-tutorials | Python/R | Tutorials |
| scArches | Python | Transfer learning |
| PathML | Python | Pathology |
| CytoCommunity | Python | Neighborhoods |
| scCube | Python | Simulation |
| STUtility | R | Visium analysis |
| STAgent | Python | Autonomous analysis |
| ChatSpatial | Python | MCP server |
| SpatialAgent | Python | AI agent |
| STAIG | Python | Graph contrastive |
| STalign | Python | Registration |
| SPIRAL | R | Integration |
| PASTE2 | Python | Alignment |
| INST-Align | Python | Neural alignment |
| GPSA | Python | GP alignment |
| CODA | Python | Diffeomorphic |
| Sutura | Python | Learned alignment |

---

## Citations

1. Rao A, Barkley D, França GS, et al. Exploring tissue architecture using spatial transcriptomics. *Nature*. 2021;596:211–220.
2. Rodriques SG, Stickels RR, Goeva A, et al. Slide-seq: a scalable technology for measuring genome-wide expression at high spatial resolution. *Science*. 2019;363:1463–1467.
3. Chen A, Liao S, Cheng M, et al. Spatiotemporal transcriptomic atlas of mouse organogenesis using DNA nanoball-patterned arrays. *Cell*. 2022;185:1777–1792.
4. Maynard C, Collado-Torres L, Weber LM, et al. Transcriptome-scale spatial gene expression in the human dorsolateral prefrontal cortex. *Nature Neuroscience*. 2021;24:425–436.
5. Ståhl PL, Salmén F, Vickovic S, et al. Visualization and analysis of gene expression in tissue sections by spatial transcriptomics. *Science*. 2016;353:78–82.
6. Tian L, Chen F, Macosko EZ. The expanding vistas of spatial transcriptomics. *Nature Biotechnology*. 2023;41:773–782.
7. Hu C, et al. Scalable spatial transcriptomics through computational array reconstruction. *Nature Biotechnology*. 2026;44:215–221.
8. Zhao E, Stone MR, Ren X, et al. Spatial transcriptomics at subspot resolution with BayesSpace. *Nature Biotechnology*. 2021;39:1375–1384.
9. Longo SK, Guo MG, Ji AL, Khavari PA. Integrating single-cell and spatial transcriptomics to elucidate intercellular tissue dynamics. *Nature Reviews Genetics*. 2021;22:627–644.
10. Kleino I. Computational solutions for spatial transcriptomics. *Briefings in Bioinformatics*. 2022;23:bbac277.
11. PMC13409801. Spatial Transcriptomics for Dissecting Cellular and Molecular Heterogeneity in the Aging and Diseased Brain.
12. PMC12071594. Spatial Omics in Clinical Research: A Comprehensive Review.
13. PMC8951701. Statistical and machine learning methods for spatially resolved transcriptomics data analysis.
14. PMC8494229. Advances in spatial transcriptomic data analysis.
15. PMC12577344. From pixels to cell types: a comprehensive review of computational methods for spatial transcriptomics deconvolution.
16. PMC13395097. SpatialPEFT: a parameter-efficient fine-tuning framework for spatial transcriptomics foundation models.
17. MDPI Cells 2025;14(14):1060. A Meta-Review of Spatial Transcriptomics Analysis Software.
18. PMC13440128. Computational analysis in spatial transcriptomics.
19. PMC11744898. A practical guide for choosing an optimal spatial transcriptomics technology.
20. PubMed 40181168. Scalable spatial transcriptomics through computational array reconstruction.
21. PubMed 35852420. Spacemake: processing and analysis of large-scale spatial transcriptomics data.
22. Vaccines 2025;14(2):158. Advances in Spatial Transcriptomics for Infectious Disease Research.
23. bioRxiv 2026.06.30.735390. Tear-collapse in spatial transcriptomics registration.
24. DOI 10.1186/s40478-026-02303-0. Spatial omics in high-grade glioma.
25. arXiv 2511.06204. DUET: Constrained convex clustering for interpretable spatial domain detection.
26. arXiv 2508.10646. SPHENIC: Topology-Aware Multi-View Clustering for Spatial Transcriptomics.
27. IJCAI 2025. TSstc: Spatially Resolved Transcriptomics Data Clustering with Tailored Spatial-scale Modulation.
28. JOSS 2025;10.21105/joss.08795. MOSAIK: Multi-Origin Spatial Transcriptomics Analysis and Integration Kit.
29. GitHub: p-gueguen/Spatial_transcriptomics_tools
30. GitHub: anthbapt/Spatial-Biology-Tools
31. GitHub: y-itao/STAIG
32. EMBL-EBI Spatial Transcriptomics Portal
33. Broad Institute News: Scaling up spatial genomics (April 3, 2025)
34. Accura Science Blog: Why Spatial Transcriptomics Analyses Fail – Part 1
35. Ion Genomics Newsletter: Illumina StrataMap Spatial Solution (June 9, 2026)
