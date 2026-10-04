"""Cross-module integration workflows for genetic engineering platform.

Provides high-level workflows that compose multiple modules:
- CRISPR design → biosecurity screening
- Protein analysis → knowledge graph storage
- Variant calling → knowledge graph storage
- Full pipeline compositions
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class WorkflowResult:
    """Result of a cross-module workflow.

    Attributes:
        grna_sequence: Designed gRNA sequence (if applicable).
        risk_level: Biosecurity risk level (if applicable).
        passed_screening: Whether the sequence passed biosecurity.
        metadata: Additional workflow-specific data.
    """

    grna_sequence: Optional[str] = None
    risk_level: Optional[str] = None
    passed_screening: Optional[bool] = None
    metadata: dict[str, Any] | None = None


class GeneticEngineeringWorkflow:
    """High-level workflows composing multiple modules.

    Usage:
        wf = GeneticEngineeringWorkflow("my_workflow")
        result = wf.run_crispr_screen("GAGTCCGAGCAGAAGAAGAAGGG")
        print(result.grna_sequence, result.risk_level)
    """

    def __init__(self, name: str) -> None:
        self.name = name

    def run_crispr_screen(self, target: str, pam: str = "NGG") -> WorkflowResult:
        """Design a gRNA and screen it for biosecurity.

        Composes: CRISPR design → Biosecurity screening.

        Args:
            target: Target DNA sequence.
            pam: PAM sequence (default NGG).

        Returns:
            WorkflowResult with gRNA sequence and risk assessment.
        """
        from src.biosecurity.screening import SequenceScreener
        from src.crispr.grna_design import design_grna

        design = design_grna(target, pam=pam)
        if design is None:
            return WorkflowResult(
                grna_sequence=None,
                risk_level=None,
                passed_screening=None,
                metadata={"error": "No valid gRNA found"},
            )

        screener = SequenceScreener()
        screen_result = screener.screen_sequence(design["sequence"])
        risk_score = screener.calculate_risk_score(design["sequence"])

        return WorkflowResult(
            grna_sequence=design["sequence"],
            risk_level="LOW" if screen_result["is_clean"] else "HIGH",
            passed_screening=screen_result["is_clean"],
            metadata={
                "efficiency": design.get("efficiency"),
                "pam": pam,
                "risk_score": risk_score,
                "matches": screen_result["matches"],
            },
        )

    def run_protein_analysis(self, sequence: str) -> dict[str, Any]:
        """Analyze a protein sequence and store results in knowledge graph.

        Composes: Protein analysis → Knowledge graph storage.

        Args:
            sequence: Amino acid sequence.

        Returns:
            Dictionary with analysis results.
        """
        from src.integration.knowledge_graph import KnowledgeGraph
        from src.protein.protein_engineering import (
            ProteinSequence,
            calculate_isoelectric_point,
            calculate_molecular_weight,
            predict_stability,
        )

        seq = ProteinSequence(sequence)
        kg = KnowledgeGraph()
        entity_id = f"protein_{hash(sequence) & 0xFFFFFFFF}"

        kg.add_entity(entity_id, "Protein", {
            "sequence": seq.sequence,
            "length": seq.length,
            "weight": calculate_molecular_weight(seq.sequence),
        })

        return {
            "entity_id": entity_id,
            "sequence": seq.sequence,
            "length": seq.length,
            "weight": calculate_molecular_weight(seq.sequence),
            "pi": calculate_isoelectric_point(seq.sequence),
            "stability": predict_stability(seq.sequence),
        }

    def run_variant_analysis(self, reference: str, reads: list[str]) -> dict[str, Any]:
        """Call variants and store results in knowledge graph.

        Composes: Variant calling → Knowledge graph storage.

        Args:
            reference: Reference genome sequence.
            reads: List of read sequences.

        Returns:
            Dictionary with variant analysis results.
        """
        from src.genomics.variant_calling import call_variants
        from src.integration.knowledge_graph import KnowledgeGraph

        variants = call_variants(reference, reads)
        kg = KnowledgeGraph()

        for i, var in enumerate(variants):
            entity_id = f"variant_{i}"
            kg.add_entity(entity_id, "Variant", {
                "chrom": var.chrom,
                "pos": var.pos,
                "ref": var.ref,
                "alt": var.alt,
                "quality": var.quality,
            })

        return {
            "variant_count": len(variants),
            "variants": [
                {"chrom": v.chrom, "pos": v.pos, "ref": v.ref, "alt": v.alt}
                for v in variants
            ],
        }

    def run_full_pipeline(self, target: str, protein_seq: str) -> dict[str, Any]:
        """Run the complete genetic engineering pipeline.

        Composes: CRISPR design → Biosecurity → Protein analysis → Storage.

        Args:
            target: Target DNA sequence for gRNA design.
            protein_seq: Protein sequence for analysis.

        Returns:
            Dictionary with all workflow results.
        """
        crispr_result = self.run_crispr_screen(target)
        protein_result = self.run_protein_analysis(protein_seq)

        return {
            "workflow_name": self.name,
            "crispr": {
                "grna": crispr_result.grna_sequence,
                "risk_level": crispr_result.risk_level,
                "passed": crispr_result.passed_screening,
            },
            "protein": protein_result,
        }
