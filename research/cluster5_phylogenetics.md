# Cluster 5: Phylogenetic Tree Reconstruction

## Overview

Phylogenetic tree reconstruction is a core computational problem in evolutionary biology, aiming to infer the evolutionary relationships among species, genes, or populations from molecular sequence data. The field spans multiple inference paradigms—maximum likelihood (ML), Bayesian inference, maximum parsimony (MP), distance-based methods, and coalescent-based species tree estimation—each with distinct computational complexity profiles, scalability characteristics, and failure modes.

---

## State-of-the-Art Approaches

1. **Maximum Likelihood (ML)**: RAxML-NG, IQ-TREE, and PhyML represent the current gold standard for ML inference. RAxML-NG is a from-scratch reimplementation of RAxML's greedy tree search, optimized for large alignments and parallel execution on workstation or cluster hardware. FastTree and VeryFastTree provide rapid approximate ML for ultra-large alignments where full ML is infeasible. [Kozlov et al., 2019, Bioinformatics](https://doi.org/10.1093/bioinformatics/btz305)

2. **Bayesian Inference**: MrBayes, BEAST2, and ExaBayes use Markov Chain Monte Carlo (MCMC) to sample from the posterior distribution of trees. BEAST2 is the primary platform for time-scaled phylogenies and phylodynamics. Bali-Phy jointly estimates alignments and trees. These methods provide uncertainty quantification but at significantly higher computational cost. [Kumar et al., 2026, Biochem Genet](https://doi.org/10.1007/s10528-026-11434-x)

3. **Maximum Parsimony (MP)**: Seeks the tree minimizing the total number of evolutionary changes. PAUP* and TNT are widely used. MP remains popular for morphological data and is the target of emerging quantum computing approaches. [Zhang & Chen, 2025, arXiv:2508.00468](https://arxiv.org/html/2508.00468v2)

4. **Coalescent-Based Species Tree Estimation**: ASTRAL estimates species trees from gene trees while accounting for incomplete lineage sorting (ILS). It is widely used in phylogenomics. [CIPRES Science Gateway](https://phylo.org/restusers/docs/tools)

5. **Distance-Based Methods**: Neighbor-Joining and FastME provide rapid tree estimation, often used as starting trees for ML optimization or for very large datasets. [Kumar et al., 2026](https://doi.org/10.1007/s10528-026-11434-x)

6. **GPU-Accelerated Likelihood Evaluation**: BEAGLE 4.1 is a high-performance library for statistical phylogenetics that evaluates sequence likelihoods and gradients across diverse parallel architectures (CPU, GPU, Intel Xeon Phi). It underlies BEAST2, MrBayes, and other frameworks. [Gangavarapu et al., 2026, arXiv:2606.27607](https://arxiv.org/pdf/2606.27607)

---

## NP-Hard Problems

1. **Maximum Parsimony Tree Reconstruction**: The problem of finding the most parsimonious tree is NP-hard, motivating heuristic search strategies and exploration of quantum computing paradigms. [Zhang & Chen, 2025](https://arxiv.org/html/2508.00468v2)

2. **Maximum Likelihood Tree Reconstruction**: Finding the optimal tree under the ML criterion is NP-hard, requiring highly optimized and scalable codes for growing empirical datasets. [Kozlov et al., 2019](https://doi.org/10.1093/bioinformatics/btz305)

3. **MP Distance Computation**: Computing the Maximum Parsimony distance between two binary phylogenetic trees is NP-hard, even when only two character states are available. An ILP formulation exists for small trees. [Kelk & Fischer, 2016, arXiv:1412.4076](https://arxiv.org/html/1412.4076v2)

4. **Dollo-k Phylogeny**: Deciding whether a Dollo-k tree exists for a binary matrix is NP-complete for any fixed k ≥ 2. The Dollo-1 (Persistent Phylogeny) problem was recently shown to be solvable in polynomial time. [Bonizzoni et al., 2017, arXiv:1611.01017](https://arxiv.org/pdf/1611.01017v2)

5. **Most Parsimonious Reconciliation with Hybridization**: Computing a maximum parsimony reconciliation for a gene tree and species network is NP-hard even when only considering deep coalescence. [LeMay et al., 2021, WABI](http://dagstuhl.sunsite.rwth-aachen.de/volltexte/2021/14354/pdf/LIPIcs-WABI-2021-1.pdf)

6. **Phylogeny Constraint Satisfaction**: Many constraint satisfaction problems on phylogenetic trees (e.g., rooted triple consistency) have been classified; some are polynomial-time solvable while others are NP-hard. [Bodlaender et al., 2017, ACM TOCL](https://doi.org/10.1145/3105907)

---

## Bottlenecks

1. **Tree Space Explosion**: The number of possible topologies for n taxa grows as (2n-5)!!, quickly exceeding astronomical numbers. For any reasonable number of taxa, exhaustive evaluation is intractable. [Kumar et al., 2026](https://doi.org/10.1007/s10528-026-11434-x)

2. **Long-Branch Attraction (LBA)**: A systematic artifact where rapidly evolving lineages are incorrectly grouped together, producing strongly supported but erroneous clades. Site-heterogeneous models (e.g., CAT-GTR) can suppress LBA. [ScienceDirect, 2020](https://www.sciencedirect.com/science/article/pii/S0960982220317553)

3. **Incomplete Lineage Sorting (ILS)**: Gene trees may differ from the species tree due to deep coalescence, particularly in rapid radiations. Coalescent-based methods (ASTRAL) address this but add computational overhead. [Galtier & Daubin, 2008, PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC2607408)

4. **Horizontal Gene Transfer (HGT)**: Pervasive in prokaryotes, HGT violates the tree-like model of evolution, making bacterial phylogeny resolution challenging despite hundreds of available genomes. [Galtier & Daubin, 2008](https://pmc.ncbi.nlm.nih.gov/articles/PMC2607408)

5. **MCMC Convergence**: Bayesian methods require MCMC sampling, which can suffer from poor mixing, especially in high-dimensional tree space. Convergence diagnostics are essential but add to computational burden. [PMC, 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC10933576)

6. **Memory Scaling**: Likelihood computation requires storing transition probabilities and conditional likelihoods for each site and each edge, scaling as O(n × m × k) for n taxa, m sites, and k states.

7. **Coalescent Model Scaling**: The BASTA likelihood scales cubically with deme count and quadratically with sequence length, limiting phylogeographic analyses to dozens of localities. [PNAS, 2026](https://www.pnas.org/doi/10.1073/pnas.2602412123)

8. **Alignment Uncertainty**: Phylogenetic inference assumes a fixed alignment, but alignment errors propagate to tree estimation. Joint alignment-tree methods (Bali-Phy) are more accurate but computationally expensive.

---

## Failure Modes

1. **Long-Branch Attraction**: Systematic error producing incorrect groupings of long branches with high bootstrap support. Mitigated by site-heterogeneous models, taxon sampling, and model selection. [PMC, 2007](https://pmc.ncbi.nlm.nih.gov/articles/PMC1796613)

2. **Systematic vs. Random Errors**: Systematic errors (model misspecification) do not decrease with more data, unlike random errors. They are the primary obstacle to phylogenetic accuracy. [ScienceDirect, 2020](https://www.sciencedirect.com/science/article/pii/S0960982220317553)

3. **Gene Tree–Species Tree Incongruence**: Caused by ILS, HGT, gene duplication/loss, and hybridization. Requires coalescent or network-based approaches rather than concatenation. [Galtier & Daubin, 2008](https://pmc.ncbi.nlm.nih.gov/articles/PMC2607408)

4. **Model Misspecification**: Using an inappropriate substitution model (e.g., Jukes-Cantor for data with rate heterogeneity) leads to biased inference. Model selection (e.g., ModelFinder in IQ-TREE) is critical.

5. **MCMC Non-Convergence**: Bayesian analyses may produce unreliable posterior distributions if chains have not converged. Requires effective sample size (ESS) checks and multiple independent runs.

6. **Terraces in Tree Space**: RAxML-NG introduced detection of "terraces"—sets of topologically distinct trees with identical likelihoods—which can trap tree search algorithms. [Kozlov et al., 2019](https://doi.org/10.1093/bioinformatics/btz305)

7. **Insufficient Taxon Sampling**: Increased taxon sampling is crucial for accuracy, but adding taxa increases computational cost super-exponentially.

8. **Alignment Errors**: Misalignments, especially in regions with indels, can produce spurious phylogenetic signal.

---

## Scalability Limits

1. **Taxon Count**: Tree space grows as (2n-5)!! for rooted binary trees. Heuristic searches become essential beyond ~20 taxa; even optimized ML tools struggle with >10,000 taxa without approximations.

2. **Sequence Length**: Likelihood computation scales linearly with sequence length, but memory requirements grow proportionally. Ultra-long alignments (e.g., whole genomes) require data partitioning or subsampling.

3. **Number of Loci**: Phylogenomic analyses with thousands of genes require concatenation (supermatrix) or coalescent-based approaches. Coalescent methods scale with the number of gene trees.

4. **Demes in Phylogeography**: Structured coalescent likelihood scales cubically with deme count, limiting analyses to dozens of regions without approximations like BASTA. [PNAS, 2026](https://www.pnas.org/doi/10.1073/pnas.2602412123)

5. **MCMC Mixing Time**: Bayesian methods require millions of MCMC iterations for adequate posterior sampling, with mixing time increasing with model complexity and data size.

6. **Parallel Scalability**: RAxML-NG and ExaBayes achieve near-linear speedup on multi-core systems, but communication overhead limits scalability on distributed clusters. [Kozlov et al., 2019](https://doi.org/10.1093/bioinformatics/btz305)

---

## Hardware Requirements

1. **GPU Acceleration**: BEAGLE 4.1 leverages NVIDIA GPUs (A100, V100) for likelihood evaluation, achieving order-of-magnitude speedups over CPU-only implementations. GPU nodes with 4× A100 (80 GB VRAM) are available on NIH Biowulf. [Gangavarapu et al., 2026](https://arxiv.org/pdf/2606.27607)

2. **HPC Clusters**: NIH Biowulf provides 1,759 compute nodes (60,876 cores, 752 GPUs) with up to 768 GB memory per node and 200 Gb/s Infiniband networking. [NIH HPC](https://hpc.nih.gov/systems/hardware.html)

3. **Memory**: Large phylogenomic alignments (e.g., 10,000 taxa × 100,000 sites) can require hundreds of GB of RAM for likelihood computation. High-memory nodes (512–768 GB) are essential.

4. **Multi-Core CPU**: RAxML-NG and IQ-TREE exploit multi-core parallelism. Nodes with 64–96 cores are standard for phylogenetic HPC.

5. **Storage**: Phylogenomic datasets (alignments, tree samples from Bayesian runs) can require terabytes of storage. Fast parallel file systems (Lustre, GPFS) are needed.

6. **Cloud/CIPRES**: The CIPRES Science Gateway provides web-based access to RAxML-NG, BEAST2, ASTRAL, and other tools on XSEDE resources, lowering the barrier to HPC access. [CIPRES](https://phylo.org/restusers/docs/tools)

---

## Cost Tradeoffs

1. **Speed vs. Accuracy**: FastTree/VeryFastTree produce approximate ML trees in minutes for ultra-large datasets, while RAxML-NG/IQ-TREE provide more accurate but slower inference. The choice depends on whether the analysis is exploratory or publication-grade. [Kumar et al., 2026](https://doi.org/10.1007/s10528-026-11434-x)

2. **Bayesian vs. ML**: Bayesian methods (BEAST2, MrBayes) provide posterior distributions and divergence time estimates but are 10–100× slower than ML. ML with bootstrap is faster but provides less nuanced uncertainty quantification.

3. **Heuristic vs. Exact**: Heuristic tree search (RAxML-NG's greedy algorithm) finds near-optimal trees efficiently but cannot guarantee global optimality. Exact methods are infeasible beyond ~20 taxa due to NP-hardness.

4. **GPU vs. CPU**: GPU acceleration (BEAGLE) requires NVIDIA hardware and CUDA but can reduce likelihood evaluation time by 10–100×. CPU-only implementations are more portable but slower.

5. **Cloud vs. Local HPC**: CIPRES provides free access to HPC for academic users but has queue wait times and data transfer overhead. Local clusters offer more control but require maintenance.

6. **Alignment Quality vs. Speed**: Joint alignment-tree inference (Bali-Phy) is more accurate than sequential alignment-then-tree but is computationally expensive. Most pipelines use fast aligners (MAFFT, ClustalW) followed by tree inference.

---

## Open Source Software Projects

1. **RAxML-NG**: Fast, scalable ML tree inference. GNU GPL. [GitHub](https://github.com/amkozlov/raxml-ng) [Kozlov et al., 2019](https://doi.org/10.1093/bioinformatics/btz305)

2. **IQ-TREE**: ML inference with automatic model selection and ultrafast bootstrap. [Nguyen et al., 2015]

3. **BEAST2**: Bayesian evolutionary analysis by sampling trees. [Bouckaert et al., 2019]

4. **MrBayes**: Bayesian phylogenetic inference using MCMC. [Ronquist et al., 2012]

5. **ASTRAL**: Coalescent-based species tree estimation from gene trees. [Mirarab et al., 2014]

6. **BEAGLE**: High-performance library for phylogenetic likelihood computation on CPUs and GPUs. [Gangavarapu et al., 2026](https://arxiv.org/pdf/2606.27607)

7. **FastTree**: Approximate ML for large alignments. [Price et al., 2010]

8. **PHYLIP**: Classical phylogenetic analysis package (parsimony, distance, likelihood). [Felsenstein, 1989]

9. **ExaBayes**: Parallel Bayesian tree inference for large datasets. [Kozlov et al., 2015]

10. **Bali-Phy**: Joint Bayesian estimation of alignment and tree. [Suchard & Redelings, 2006]

11. **PhyloZoo**: Python package for phylogenetic network analysis. [Holtgreve, 2026](https://www.nielsholtgrefe.nl/software/)

12. **Squirrel**: Phylogenetic network reconstruction from DNA alignments. [Holtgreve, 2026](https://www.nielsholtgrefe.nl/software/)

13. **CIPRES Science Gateway**: Web portal providing access to 30+ phylogenetic tools on XSEDE HPC resources. [CIPRES](https://phylo.org/restusers/docs/tools)

14. **PhyloProfile v2**: Scalable exploration of phylogenetic profiles via dimensionality reduction. [Tran & Ebersberger, 2025, arXiv:2504.19710](https://arxiv.org/pdf/2504.19710)

---

## Biosecurity Governance

1. **Dual-Use Research of Concern (DURC)**: Phylogenetic research on pathogens has dual-use potential—it can inform public health responses but could also be misused to engineer or enhance pathogens. The US government has established DURC policies to manage dissemination of sensitive life sciences research. [NCBI Bookshelf](https://www.ncbi.nlm.nih.gov/books/NBK458495/)

2. **Ethical Frameworks**: The dual-use dilemma in the life sciences requires balancing scientific openness against security concerns. Phylogenetic studies of viral pathogens (e.g., SARS-CoV-2, avian influenza) are particularly sensitive. [PMC, 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7089176)

3. **Pathogen Phylogeography**: Reconstructing spatiotemporal transmission dynamics of pathogens (e.g., H5N1, dengue) is essential for epidemic preparedness but raises biosecurity concerns about revealing vulnerabilities or enabling targeted interventions. [PNAS, 2026](https://www.pnas.org/doi/10.1073/pnas.2602412123)

4. **Genetic Engineering Concerns**: Advances in genetic engineering of pathogenic microorganisms have heightened biosecurity concerns. Phylogenetic tools could theoretically be applied to infer evolutionary trajectories of engineered pathogens. [NCBI Bookshelf](https://www.ncbi.nlm.nih.gov/books/NBK458495/)

5. **Governance Tension**: There is growing tension between scientific transparency (essential for reproducibility and collaboration) and the need to restrict information that could be exploited by malicious actors. Current governance relies on institutional review, funding agency guidelines, and journal policies. [CSS ETH Zurich](https://css.ethz.ch/en/center/CSS-news/2017/10/the-dual-use-dilemma-in-the-life-sciences.html)

---

## Most Cited Papers

1. **Kozlov, A.M., Darriba, D., Flouri, T., Morel, B., Stamatakis, A.** (2019). RAxML-NG: a fast, scalable and user-friendly tool for maximum likelihood phylogenetic inference. *Bioinformatics*, 35(21), 4453–4455. [DOI: 10.1093/bioinformatics/btz305](https://doi.org/10.1093/bioinformatics/btz305)

2. **Gangavarapu, K., Ji, X., Shao, Y., Lemey, P., Rambaut, A., Baele, G., Suchard, M.A.** (2026). BEAGLE 4.1: A high-performance library for computation on phylogenetic trees across diverse parallel architectures. *arXiv:2606.27607*. [arXiv](https://arxiv.org/pdf/2606.27607)

3. **Kumar, A., Dakal, T.C., Parveen, K., et al.** (2026). Revisiting Algorithms, Tools, and Applications for Sequence and Phylogenetic Analyses in the NGS-Based Omics Era. *Biochemical Genetics*. [DOI: 10.1007/s10528-026-11434-x](https://doi.org/10.1007/s10528-026-11434-x)

4. **Kelk, S., Fischer, M.** (2016). On the complexity of computing MP distance between binary phylogenetic trees. *arXiv:1412.4076*. [arXiv](https://arxiv.org/html/1412.4076v2)

5. **Bodlaender, H.L., Fellows, M.R., Hallett, M.T., et al.** (2017). The Complexity of Phylogeny Constraint Satisfaction Problems. *ACM Transactions on Computational Logic*, 18(3), 23. [DOI: 10.1145/3105907](https://doi.org/10.1145/3105907)

6. **Bonizzoni, P., Della Vedova, G., Gomez, M.S., Trucco, G.** (2017). On Computing the Dollo-1 phylogeny in polynomial time. *arXiv:1611.01017*. [arXiv](https://arxiv.org/pdf/1611.01017v2)

7. **LeMay, M., Wu, Y.-C., Libeskind-Hadas, R.** (2021). The Most Parsimonious Reconciliation Problem in the Presence of Incomplete Lineage Sorting and Hybridization Is NP-Hard. *WABI 2021*. [Dagstuhl](http://dagstuhl.sunsite.rwth-aachen.de/volltexte/2021/14354/pdf/LIPIcs-WABI-2021-1.pdf)

8. **Zhang, J., Chen, Y.** (2025). Inference of maximum parsimony phylogenetic trees with model-based classical and quantum methods. *arXiv:2508.00468*. [arXiv](https://arxiv.org/html/2508.00468v2)

9. **Tran, V., Ebersberger, I.** (2025). PhyloProfile v2: Scalable Exploration of Multi-layered Phylogenetic Profiles via Dimensionality Reduction. *arXiv:2504.19710*. [arXiv](https://arxiv.org/pdf/2504.19710)

10. **Galtier, N., Daubin, V.** (2008). Dealing with incongruence in phylogenomic analyses. *PMC*. [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC2607408)

---

## Summary

Phylogenetic tree reconstruction is a computationally intensive field characterized by NP-hard core problems, rapid growth of tree space with taxon count, and diverse failure modes including long-branch attraction and gene tree–species tree incongruence. State-of-the-art tools (RAxML-NG, IQ-TREE, BEAST2, ASTRAL) leverage GPU acceleration and HPC parallelism to handle increasingly large datasets, but fundamental scalability limits remain. The field is actively exploring quantum computing for MP inference, GPU-accelerated likelihood evaluation (BEAGLE 4.1), and parallel coalescent methods for phylogeography. Biosecurity governance is an emerging concern, particularly for pathogen phylogenetics with dual-use potential.
