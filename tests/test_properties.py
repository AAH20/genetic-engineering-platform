"""Property-based tests for algorithmic invariants across modules."""
import pytest

hypothesis = pytest.importorskip("hypothesis")
from hypothesis import given, settings  # noqa: E402
from hypothesis import strategies as st


class TestCrisprProperties:
    """Property-based invariants for CRISPR module."""

    @given(st.text(alphabet="ACGT", min_size=20, max_size=100))
    @settings(max_examples=50)
    def test_gc_content_bounds(self, seq):
        from src.crispr.grna_design import calculate_gc_content
        gc = calculate_gc_content(seq)
        assert 0.0 <= gc <= 1.0

    @given(st.text(alphabet="ACGT", min_size=20, max_size=20))
    @settings(max_examples=50)
    def test_grna_validation_exact_length(self, seq):
        from src.crispr.grna_design import validate_grna_sequence
        assert validate_grna_sequence(seq) is True

    @given(st.text(alphabet="ACGT", min_size=0, max_size=19))
    @settings(max_examples=30)
    def test_short_sequences_rejected(self, seq):
        from src.crispr.grna_design import validate_grna_sequence
        if len(seq) != 20:
            assert validate_grna_sequence(seq) is False

    @given(st.text(alphabet="ACGT", min_size=21, max_size=50))
    @settings(max_examples=30)
    def test_long_sequences_rejected(self, seq):
        from src.crispr.grna_design import validate_grna_sequence
        assert validate_grna_sequence(seq) is False


class TestProteinProperties:
    """Property-based invariants for Protein module."""

    @given(st.text(alphabet="ACDEFGHIKLMNPQRSTVWY", min_size=1, max_size=100))
    @settings(max_examples=50)
    def test_molecular_weight_positive(self, seq):
        from src.protein.protein_engineering import calculate_molecular_weight
        assert calculate_molecular_weight(seq) > 0

    @given(st.text(alphabet="ACDEFGHIKLMNPQRSTVWY", min_size=1, max_size=100))
    @settings(max_examples=50)
    def test_pi_in_valid_range(self, seq):
        from src.protein.protein_engineering import calculate_isoelectric_point
        pi = calculate_isoelectric_point(seq)
        assert 3.0 <= pi <= 12.0

    @given(st.text(alphabet="ACDEFGHIKLMNPQRSTVWY", min_size=1, max_size=100))
    @settings(max_examples=50)
    def test_stability_in_range(self, seq):
        from src.protein.protein_engineering import predict_stability
        stability = predict_stability(seq)
        assert 0.0 <= stability <= 1.0

    @given(st.text(alphabet="ACDEFGHIKLMNPQRSTVWY", min_size=1, max_size=50))
    @settings(max_examples=30)
    def test_longer_sequences_heavier(self, short_seq):
        from src.protein.protein_engineering import calculate_molecular_weight
        long_seq = short_seq + "A"
        assert calculate_molecular_weight(long_seq) >= calculate_molecular_weight(short_seq)


class TestGenomicsProperties:
    """Property-based invariants for Genomics module."""

    @given(st.integers(min_value=0, max_value=1000), st.integers(min_value=1, max_value=1000))
    @settings(max_examples=50)
    def test_vaf_bounds(self, alt, total):
        from src.genomics.variant_calling import calculate_vaf
        vaf = calculate_vaf(alt, total)
        assert 0.0 <= vaf <= 1.0

    @given(st.integers(min_value=0, max_value=100), st.integers(min_value=1, max_value=100))
    @settings(max_examples=30)
    def test_vaf_zero_when_no_alt(self, alt, total):
        from src.genomics.variant_calling import calculate_vaf
        if alt == 0:
            assert calculate_vaf(alt, total) == 0.0

    @given(st.integers(min_value=1, max_value=100), st.integers(min_value=1, max_value=100))
    @settings(max_examples=30)
    def test_vaf_one_when_all_alt(self, alt, total):
        from src.genomics.variant_calling import calculate_vaf
        if alt >= total:
            assert calculate_vaf(alt, total) == 1.0


class TestMetabolicProperties:
    """Property-based invariants for Metabolic module."""

    @given(st.text(alphabet="ACGT", min_size=10, max_size=100))
    @settings(max_examples=30)
    def test_pathway_yield_nonnegative(self, seq):
        from src.metabolic.fba import MetabolicModel, PathwayDesigner
        model = MetabolicModel()
        model.add_reaction("R1", {"A": -1, "B": 1}, 0.0, 100.0)
        model.add_reaction("R2", {"B": -1, "C": 1}, 0.0, 100.0)
        designer = PathwayDesigner(model)
        pathway = designer.design_pathway("A", "C")
        if pathway:
            y = designer.calculate_pathway_yield(pathway)
            assert y >= 0.0

    @given(st.text(alphabet="ACGT", min_size=10, max_size=100))
    @settings(max_examples=30)
    def test_fba_fluxes_within_bounds(self, seq):
        from src.metabolic.fba import MetabolicModel
        model = MetabolicModel()
        model.add_reaction("R1", {"A": -1, "B": 1}, 0.0, 50.0)
        model.add_reaction("R2", {"B": -1, "C": 1}, 0.0, 50.0)
        model.add_reaction("R3", {"C": -1}, 0.0, 50.0)
        model.set_objective("R3")
        fluxes = model.solve_fba()
        for rxn_name, flux in fluxes.items():
            rxn = model.reactions[rxn_name]
            assert rxn.lower_bound <= flux <= rxn.upper_bound


class TestBiosecurityProperties:
    """Property-based invariants for Biosecurity module."""

    @given(st.text(alphabet="ACGT", min_size=0, max_size=100))
    @settings(max_examples=50)
    def test_risk_score_bounds(self, seq):
        from src.biosecurity.screening import SequenceScreener
        screener = SequenceScreener()
        score = screener.calculate_risk_score(seq)
        assert 0.0 <= score <= 1.0

    @given(st.text(alphabet="ACGT", min_size=0, max_size=100))
    @settings(max_examples=30)
    def test_clean_sequence_low_risk(self, seq):
        from src.biosecurity.screening import SequenceScreener
        screener = SequenceScreener()
        result = screener.screen_sequence(seq)
        assert isinstance(result["is_clean"], bool)
        assert isinstance(result["matches"], list)


class TestIntegrationProperties:
    """Property-based invariants for Integration module."""

    @given(st.text(alphabet="ACGT", min_size=1, max_size=50))
    @settings(max_examples=30)
    def test_knowledge_graph_roundtrip(self, seq):
        from src.integration.knowledge_graph import KnowledgeGraph
        kg = KnowledgeGraph()
        kg.add_entity("e1", "Type", {"seq": seq})
        results = kg.query(type="Type")
        assert "e1" in results
        assert results["e1"]["properties"]["seq"] == seq

    @given(st.integers(min_value=100, max_value=10000))
    @settings(max_examples=30)
    def test_digital_twin_simulation_changes_state(self, initial):
        from src.integration.knowledge_graph import DigitalTwin
        twin = DigitalTwin("test")
        twin.update_state("cell_count", initial)
        twin.simulate(steps=1)
        assert twin.get_state("cell_count") != initial
