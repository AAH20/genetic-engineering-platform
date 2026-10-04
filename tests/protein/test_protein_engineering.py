"""Test-driven development: Protein Engineering module."""
import pytest

from src.protein.protein_engineering import (
    AMINO_ACID_WEIGHTS,
    VALID_AMINO_ACIDS,
    ProteinSequence,
    ProteinStructure,
    calculate_isoelectric_point,
    calculate_molecular_weight,
    design_sequence,
    predict_stability,
    predict_structure,
)


class TestProteinSequenceValidation:
    """Test ProteinSequence validation."""

    def test_valid_sequence(self):
        """A valid amino acid sequence should be accepted."""
        seq = ProteinSequence("ACDEFGHIKLMNPQRSTVWY")
        assert seq.sequence == "ACDEFGHIKLMNPQRSTVWY"
        assert seq.length == 20

    def test_valid_sequence_lowercase(self):
        """Lowercase sequence should be normalized to uppercase."""
        seq = ProteinSequence("acdefghiklmnpqrstvwy")
        assert seq.sequence == "ACDEFGHIKLMNPQRSTVWY"

    def test_invalid_amino_acid(self):
        """Sequence with invalid amino acid should raise ValueError."""
        with pytest.raises(ValueError):
            ProteinSequence("ACDEFGHIKLMNPQRSTVWYX")

    def test_empty_sequence(self):
        """Empty sequence should raise ValueError."""
        with pytest.raises(ValueError):
            ProteinSequence("")

    def test_single_amino_acid(self):
        """Single amino acid should be valid."""
        seq = ProteinSequence("A")
        assert seq.length == 1

    def test_whitespace_rejected(self):
        """Sequence with whitespace should raise ValueError."""
        with pytest.raises(ValueError):
            ProteinSequence("ACDEFGHIKLMNPQRSTVWY ")

    def test_non_string_input(self):
        """Non-string input should raise TypeError."""
        with pytest.raises(TypeError):
            ProteinSequence(123)

    def test_max_length_boundary(self):
        """Sequence at max length should be valid."""
        seq = ProteinSequence("A" * 5000)
        assert seq.length == 5000

    def test_exceeds_max_length(self):
        """Sequence exceeding max length should raise ValueError."""
        with pytest.raises(ValueError):
            ProteinSequence("A" * 5001)


class TestMolecularWeight:
    """Test molecular weight calculation."""

    def test_single_amino_acid_weight(self):
        """Weight of single amino acid should match."""
        assert calculate_molecular_weight("A") == pytest.approx(89.1)

    def test_known_sequence_weight(self):
        """Weight of a known sequence should be sum of weights."""
        seq = "AG"
        expected = 89.1 + 75.0
        assert calculate_molecular_weight(seq) == pytest.approx(expected)

    def test_empty_sequence_weight(self):
        """Empty sequence should return 0.0."""
        assert calculate_molecular_weight("") == 0.0

    def test_invalid_sequence_raises(self):
        """Invalid sequence should raise ValueError."""
        with pytest.raises(ValueError):
            calculate_molecular_weight("ACDEFGHIKLMNPQRSTVWYX")

    def test_case_insensitive(self):
        """Weight calculation should be case-insensitive."""
        assert calculate_molecular_weight("ag") == calculate_molecular_weight("AG")

    def test_all_amino_acids_weight(self):
        """Weight of all 20 amino acids should be sum of all weights."""
        all_aa = "ACDEFGHIKLMNPQRSTVWY"
        expected = sum(AMINO_ACID_WEIGHTS.values())
        assert calculate_molecular_weight(all_aa) == pytest.approx(expected)


class TestIsoelectricPoint:
    """Test isoelectric point calculation."""

    def test_neutral_sequence(self):
        """Sequence with equal acidic and basic residues should have pI near 7."""
        seq = "DEKR"  # 2 acidic, 2 basic
        pi = calculate_isoelectric_point(seq)
        assert 5.0 <= pi <= 9.0

    def test_acidic_sequence(self):
        """Acidic sequence should have low pI."""
        seq = "DDEE"
        pi = calculate_isoelectric_point(seq)
        assert pi < 7.0

    def test_basic_sequence(self):
        """Basic sequence should have high pI."""
        seq = "KKRR"
        pi = calculate_isoelectric_point(seq)
        assert pi > 7.0

    def test_empty_sequence(self):
        """Empty sequence should return neutral pI."""
        assert calculate_isoelectric_point("") == pytest.approx(7.0)

    def test_invalid_sequence_raises(self):
        """Invalid sequence should raise ValueError."""
        with pytest.raises(ValueError):
            calculate_isoelectric_point("ACDEFGHIKLMNPQRSTVWYX")

    def test_pi_range(self):
        """pI should be within reasonable range."""
        seq = "ACDEFGHIKLMNPQRSTVWY"
        pi = calculate_isoelectric_point(seq)
        assert 3.0 <= pi <= 12.0


class TestStabilityPrediction:
    """Test stability prediction."""

    def test_high_hydrophobic_stable(self):
        """High hydrophobic ratio should yield high stability."""
        seq = "AVILMFWP"  # all hydrophobic
        stability = predict_stability(seq)
        assert stability > 0.5

    def test_low_hydrophobic_unstable(self):
        """Low hydrophobic ratio should yield low stability."""
        seq = "DEKRHNQ"  # all hydrophilic
        stability = predict_stability(seq)
        assert stability < 0.5

    def test_empty_sequence(self):
        """Empty sequence should return 0.0 stability."""
        assert predict_stability("") == 0.0

    def test_invalid_sequence_raises(self):
        """Invalid sequence should raise ValueError."""
        with pytest.raises(ValueError):
            predict_stability("ACDEFGHIKLMNPQRSTVWYX")

    def test_stability_range(self):
        """Stability should be between 0 and 1."""
        seq = "ACDEFGHIKLMNPQRSTVWY"
        stability = predict_stability(seq)
        assert 0.0 <= stability <= 1.0

    def test_mixed_sequence(self):
        """Mixed sequence should have moderate stability."""
        seq = "AVILDEKR"
        stability = predict_stability(seq)
        assert 0.0 < stability < 1.0


class TestSequenceDesign:
    """Test sequence design."""

    def test_design_returns_valid_sequence(self):
        """Designed sequence should be valid."""
        seq = design_sequence(target_length=20, target_hydrophobic_ratio=0.5)
        assert len(seq) == 20
        assert all(c in VALID_AMINO_ACIDS for c in seq)

    def test_design_respects_length(self):
        """Designed sequence should have target length."""
        seq = design_sequence(target_length=50, target_hydrophobic_ratio=0.3)
        assert len(seq) == 50

    def test_design_respects_hydrophobic_ratio(self):
        """Designed sequence should approximate target hydrophobic ratio."""
        target_ratio = 0.7
        seq = design_sequence(target_length=100, target_hydrophobic_ratio=target_ratio)
        hydrophobic = set("AVILMFWPG")
        actual_ratio = sum(1 for c in seq if c in hydrophobic) / len(seq)
        assert abs(actual_ratio - target_ratio) < 0.15

    def test_design_empty_length(self):
        """Design with zero length should return empty string."""
        seq = design_sequence(target_length=0, target_hydrophobic_ratio=0.5)
        assert seq == ""

    def test_design_invalid_length(self):
        """Design with negative length should raise ValueError."""
        with pytest.raises(ValueError):
            design_sequence(target_length=-1, target_hydrophobic_ratio=0.5)

    def test_design_invalid_ratio(self):
        """Design with invalid hydrophobic ratio should raise ValueError."""
        with pytest.raises(ValueError):
            design_sequence(target_length=20, target_hydrophobic_ratio=1.5)


class TestProteinStructure:
    """Test ProteinStructure class."""

    def test_valid_structure(self):
        """Valid structure should be created."""
        struct = ProteinStructure("ACDEFGHIKLMNPQRSTVWY", "alpha")
        assert struct.sequence == "ACDEFGHIKLMNPQRSTVWY"
        assert struct.structure_type == "alpha"

    def test_invalid_structure_type(self):
        """Invalid structure type should raise ValueError."""
        with pytest.raises(ValueError):
            ProteinStructure("ACDEFGHIKLMNPQRSTVWY", "invalid")

    def test_invalid_sequence_raises(self):
        """Invalid sequence should raise ValueError."""
        with pytest.raises(ValueError):
            ProteinStructure("ACDEFGHIKLMNPQRSTVWYX", "alpha")

    def test_structure_types(self):
        """All valid structure types should be accepted."""
        for stype in ["alpha", "beta", "mixed"]:
            struct = ProteinStructure("ACDEFGHIKLMNPQRSTVWY", stype)
            assert struct.structure_type == stype


class TestStructurePrediction:
    """Test structure prediction."""

    def test_alpha_helix_prediction(self):
        """Alpha-helix favoring sequence should predict alpha."""
        seq = "AELKAMELKAMELKAMELKA"  # alpha-helix favoring
        assert predict_structure(seq) == "alpha"

    def test_beta_sheet_prediction(self):
        """Beta-sheet favoring sequence should predict beta."""
        seq = "VIFYWTVIFYWTVIFYWTV"  # beta-sheet favoring
        assert predict_structure(seq) == "beta"

    def test_mixed_prediction(self):
        """Mixed sequence should predict mixed."""
        seq = "ACDEFGHIKLMNPQRSTVWY"
        result = predict_structure(seq)
        assert result in ["alpha", "beta", "mixed"]

    def test_empty_sequence(self):
        """Empty sequence should return 'mixed'."""
        assert predict_structure("") == "mixed"

    def test_invalid_sequence_raises(self):
        """Invalid sequence should raise ValueError."""
        with pytest.raises(ValueError):
            predict_structure("ACDEFGHIKLMNPQRSTVWYX")

    def test_prediction_valid_types(self):
        """Prediction should always return valid structure type."""
        seq = "ACDEFGHIKLMNPQRSTVWY"
        result = predict_structure(seq)
        assert result in ["alpha", "beta", "mixed"]
