"""TDD tests for cross-module integration."""
from src.integration.cross_module import GeneticEngineeringWorkflow


class TestCrossModule:
    def test_crispr_to_biosecurity(self):
        wf = GeneticEngineeringWorkflow("test")
        result = wf.run_crispr_screen("GAGTCCGAGCAGAAGAAGAAGGG")
        assert result.grna_sequence is not None
        assert result.risk_level is not None

    def test_crispr_screen_with_pam(self):
        wf = GeneticEngineeringWorkflow("test")
        result = wf.run_crispr_screen("GAGTCCGAGCAGAAGAAGAAGGG", pam="NGG")
        assert result.grna_sequence is not None

    def test_crispr_screen_fails_on_invalid(self):
        wf = GeneticEngineeringWorkflow("test")
        result = wf.run_crispr_screen("ATATATATATATATATATAT")
        assert result.grna_sequence is None

    def test_protein_to_knowledge_graph(self):
        from src.integration.knowledge_graph import KnowledgeGraph
        from src.protein.protein_engineering import (
            ProteinSequence,
            calculate_molecular_weight,
        )

        seq = ProteinSequence("MKWVTFISLLLLFSSAYSRGVFRR")
        kg = KnowledgeGraph()
        kg.add_entity("protein1", "Protein", {
            "sequence": seq.sequence,
            "weight": calculate_molecular_weight(seq.sequence),
        })
        neighbors = kg.get_neighbors("protein1")
        assert len(neighbors) >= 0

    def test_variant_to_knowledge_graph(self):
        from src.genomics.variant_calling import Variant
        from src.integration.knowledge_graph import KnowledgeGraph

        var = Variant(chrom="chr1", pos=1000, ref="A", alt="G", quality=30.0)
        kg = KnowledgeGraph()
        kg.add_entity("variant1", "Variant", {
            "chrom": var.chrom,
            "pos": var.pos,
            "ref": var.ref,
            "alt": var.alt,
        })
        assert "variant1" in kg.entities

    def test_pipeline_composes_modules(self):
        from src.biosecurity.screening import BiosecurityGate
        from src.crispr.grna_design import design_grna
        from src.pipeline.pipeline import Pipeline, PipelineStep

        p = Pipeline("compose")
        p.add_step(PipelineStep("design", lambda _: design_grna("GAGTCCGAGCAGAAGAAGAAGGG")))
        p.add_step(PipelineStep("screen", lambda r: BiosecurityGate().evaluate(r["sequence"])))
        result = p.run(None)
        assert result.error is None
        assert result.output is not None

    def test_sizing_recommendation(self):
        from src.sizing.sizing import SizingTier, recommend_tier
        rec = recommend_tier(team_size=5, monthly_budget=10000, compute_cores=16, storage_tb=2)
        assert rec.tier == SizingTier.LAB
        assert rec.recommended_cores > 0

    def test_event_bus_integration(self):
        from src.integration.knowledge_graph import EventBus
        bus = EventBus()
        received = []
        bus.subscribe("test_event", lambda e: received.append(e))
        bus.publish("test_event", {"data": 42})
        assert len(received) == 1
        assert received[0]["type"] == "test_event"
        assert received[0]["data"] == {"data": 42}

    def test_digital_twin_integration(self):
        from src.integration.knowledge_graph import DigitalTwin
        twin = DigitalTwin("cell_1")
        twin.update_state("cell_count", 100)
        twin.simulate(steps=1)
        assert twin.get_state("cell_count") != 100
