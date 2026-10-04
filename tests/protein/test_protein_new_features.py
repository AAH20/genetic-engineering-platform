"""TDD tests for new Protein Engineering features."""
from src.protein.protein_engineering import (
    ProteinSequence,
    calculate_charge_at_ph,
    identify_domains,
    predict_signal_peptide,
)


class TestProteinSequenceMethods:
    """Test convenience methods on ProteinSequence class."""

    def test_molecular_weight_property(self):
        seq = ProteinSequence("ACDEFGHIKLMNPQRSTVWY")
        assert seq.molecular_weight > 0
        assert abs(seq.molecular_weight - 2737.9) < 1.0

    def test_isoelectric_point_property(self):
        seq = ProteinSequence("ACDEFGHIKLMNPQRSTVWY")
        assert 3.0 <= seq.isoelectric_point <= 12.0

    def test_stability_property(self):
        seq = ProteinSequence("ACDEFGHIKLMNPQRSTVWY")
        assert 0.0 <= seq.stability <= 1.0

    def test_structure_property(self):
        seq = ProteinSequence("ACDEFGHIKLMNPQRSTVWY")
        assert seq.structure in {"alpha", "beta", "mixed"}

    def test_to_dict(self):
        seq = ProteinSequence("ACDEFGHIKLMNPQRSTVWY")
        d = seq.to_dict()
        assert d["sequence"] == "ACDEFGHIKLMNPQRSTVWY"
        assert d["length"] == 20
        assert d["weight"] > 0
        assert "pi" in d
        assert "stability" in d
        assert "structure" in d


class TestDomainIdentification:
    """Test domain identification from sequence."""

    def test_no_domains_short_sequence(self):
        domains = identify_domains("ACDEFGHIKLMNPQRSTVWY")
        assert isinstance(domains, list)

    def test_domains_found_in_long_hydrophobic(self):
        seq = "AAAA" + "ACDEFGHIKLMNPQRSTVWY" * 5 + "VVVV"
        domains = identify_domains(seq)
        assert isinstance(domains, list)

    def test_domains_have_start_end(self):
        seq = "ACDEFGHIKLMNPQRSTVWY" * 10
        domains = identify_domains(seq)
        for d in domains:
            assert "start" in d
            assert "end" in d
            assert "type" in d
            assert d["start"] < d["end"]

    def test_empty_sequence(self):
        assert identify_domains("") == []


class TestSignalPeptidePrediction:
    """Test signal peptide prediction."""

    def test_no_signal_peptide(self):
        result = predict_signal_peptide("ACDEFGHIKLMNPQRSTVWY")
        assert result["has_signal"] is False

    def test_signal_peptide_detected(self):
        seq = "MKWVTFISLLLLFSSAYSRGVFRR" + "ACDEFGHIKLMNPQRSTVWY" * 3
        result = predict_signal_peptide(seq)
        assert result["has_signal"] is True
        assert result["cleavage_site"] > 0

    def test_empty_sequence(self):
        result = predict_signal_peptide("")
        assert result["has_signal"] is False

    def test_short_sequence(self):
        result = predict_signal_peptide("ACDEFGHIKLMNPQRSTVWY")
        assert result["has_signal"] is False


class TestChargeAtPH:
    """Test charge calculation at given pH."""

    def test_neutral_ph(self):
        charge = calculate_charge_at_ph("ACDEFGHIKLMNPQRSTVWY", 7.0)
        assert isinstance(charge, float)

    def test_acidic_ph(self):
        charge = calculate_charge_at_ph("ACDEFGHIKLMNPQRSTVWY", 3.0)
        assert charge > 0

    def test_basic_ph(self):
        charge = calculate_charge_at_ph("ACDEFGHIKLMNPQRSTVWY", 11.0)
        assert charge < 0

    def test_empty_sequence(self):
        assert calculate_charge_at_ph("", 7.0) == 0.0
