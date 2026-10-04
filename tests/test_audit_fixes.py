"""Regression tests for audit-identified bug fixes."""


class TestBiosecurityReverseComplement:
    """Biosecurity must screen both strands."""

    def test_forward_strand_detected(self):
        from src.biosecurity.screening import SequenceScreener
        screener = SequenceScreener()
        result = screener.screen_sequence("GAGCTGCTGGACTTCGCT")
        assert result["is_clean"] is False
        assert "botulinum_neurotoxin_light_chain" in result["matches"]

    def test_reverse_complement_detected(self):
        from src.biosecurity.screening import SequenceScreener
        screener = SequenceScreener()
        # Reverse complement of "GAGCTGCTGGACTTCGCT" is "AGCGAAGTCCAGCAGCTC"
        result = screener.screen_sequence("AGCGAAGTCCAGCAGCTC")
        assert result["is_clean"] is False
        assert "botulinum_neurotoxin_light_chain" in result["matches"]

    def test_risk_score_includes_reverse_complement(self):
        from src.biosecurity.screening import SequenceScreener
        screener = SequenceScreener()
        rc_seq = "AGCGAAGTCCAGCAGCTC"
        score = screener.calculate_risk_score(rc_seq)
        assert score > 0.0

    def test_clean_sequence_passes(self):
        from src.biosecurity.screening import SequenceScreener
        screener = SequenceScreener()
        result = screener.screen_sequence("ATGCATGCATGCATGCATGC")
        assert result["is_clean"] is True


class TestKnowledgeGraphIndexing:
    """KnowledgeGraph must use O(1) indexed queries."""

    def test_query_by_type_uses_index(self):
        from src.integration.knowledge_graph import KnowledgeGraph
        kg = KnowledgeGraph()
        kg.add_entity("e1", "TypeA", {"x": 1})
        kg.add_entity("e2", "TypeB", {"x": 2})
        kg.add_entity("e3", "TypeA", {"x": 3})
        results = kg.query(type="TypeA")
        assert "e1" in results
        assert "e3" in results
        assert "e2" not in results

    def test_get_neighbors_uses_index(self):
        from src.integration.knowledge_graph import KnowledgeGraph
        kg = KnowledgeGraph()
        kg.add_entity("e1", "TypeA")
        kg.add_entity("e2", "TypeB")
        kg.add_entity("e3", "TypeC")
        kg.add_relation("e1", "rel", "e2")
        kg.add_relation("e1", "rel", "e3")
        neighbors = kg.get_neighbors("e1")
        assert "e2" in neighbors
        assert "e3" in neighbors

    def test_type_index_updated_on_add(self):
        from src.integration.knowledge_graph import KnowledgeGraph
        kg = KnowledgeGraph()
        kg.add_entity("e1", "TypeA")
        assert "e1" in kg._type_index.get("TypeA", set())


class TestEventBusMaxEvents:
    """EventBus must evict old events when max_events exceeded."""

    def test_events_evicted(self):
        from src.integration.knowledge_graph import EventBus
        bus = EventBus(max_events=5)
        for i in range(10):
            bus.publish("test", {"i": i})
        events = bus.get_events("test")
        assert len(events) == 5
        assert events[-1]["data"]["i"] == 9

    def test_no_eviction_under_limit(self):
        from src.integration.knowledge_graph import EventBus
        bus = EventBus(max_events=100)
        for i in range(10):
            bus.publish("test", {"i": i})
        events = bus.get_events("test")
        assert len(events) == 10


class TestPipelineSignatureInspection:
    """PipelineStep must inspect function signature."""

    def test_single_arg_function(self):
        from src.pipeline.pipeline import PipelineStep
        step = PipelineStep("double", lambda x: x * 2)
        result = step.execute(5, context={"key": "value"})
        assert result == 10

    def test_two_arg_function(self):
        from src.pipeline.pipeline import PipelineStep
        step = PipelineStep("add", lambda x, ctx: x + ctx["value"])
        result = step.execute(5, context={"value": 3})
        assert result == 8


class TestGeneTherapyDeliveryRoutes:
    """Gene therapy delivery routes must be clinically correct."""

    def test_lung_delivery(self):
        from src.genetherapy.vector_design import optimize_delivery
        route = optimize_delivery("lung", "AAV9", 30)
        assert route == "inhalation"

    def test_eye_delivery(self):
        from src.genetherapy.vector_design import optimize_delivery
        route = optimize_delivery("eye", "AAV2", 30)
        assert route == "intravitreal"

    def test_brain_delivery(self):
        from src.genetherapy.vector_design import optimize_delivery
        route = optimize_delivery("brain", "AAV9", 30)
        assert route == "IT"


class TestCRISPRMaxOffTargets:
    """design_grna must include max_off_targets in return dict."""

    def test_max_off_targets_in_result(self):
        from src.crispr.grna_design import design_grna
        target = "GAGTCCGAGCAGAAGAAGAA" + "GGG"
        result = design_grna(target, max_off_targets=50)
        assert result is not None
        assert result["max_off_targets"] == 50


class TestRiskLevelCasing:
    """Risk levels must use title case consistently."""

    def test_cross_module_risk_level(self):
        from src.integration.cross_module import GeneticEngineeringWorkflow
        wf = GeneticEngineeringWorkflow("test")
        result = wf.run_crispr_screen("GAGTCCGAGCAGAAGAAGAAGGG")
        if result.risk_level is not None:
            assert result.risk_level in {"Low", "Medium", "High", "Extreme"}

    def test_biosecurity_gate_risk_level(self):
        from src.biosecurity.screening import BiosecurityGate
        gate = BiosecurityGate()
        result = gate.evaluate("ATGCATGCATGCATGCATGC")
        assert result["risk_level"] in {"Low", "Medium", "High", "Extreme"}
