"""Comprehensive tests for biosecurity screening module."""
from src.biosecurity.screening import (
    BiosecurityGate,
    ComplianceChecker,
    DualUseDetector,
    SequenceScreener,
)


# ---------------------------------------------------------------------------
# SequenceScreener tests
# ---------------------------------------------------------------------------
class TestSequenceScreener:
    def setup_method(self):
        self.screener = SequenceScreener()

    # --- screen_sequence ---
    def test_screen_clean_sequence(self):
        seq = "ATGCGTACGTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGC"
        result = self.screener.screen_sequence(seq)
        assert isinstance(result, dict)
        assert result["is_clean"] is True
        assert result["matches"] == []

    def test_screen_threat_sequence(self):
        seq = "ATGGAGCTGCTGGACTTCGCTATCGAGCTGCTGGACTTCGCTATCGAGCTGCTGGACTTC"
        result = self.screener.screen_sequence(seq)
        assert result["is_clean"] is False
        assert len(result["matches"]) > 0

    def test_screen_multiple_threats(self):
        seq = (
            "ATGGAGCTGCTGGACTTCGCTATCGAGCTGCTGGACTTCGCT"
            "ATGCGTACGTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGC"
            "ATGTTCGCTGCTGCTGCTGCTGCTGCTGCTGCTGCTGCTGC"
        )
        result = self.screener.screen_sequence(seq)
        assert result["is_clean"] is False
        assert len(result["matches"]) >= 1

    def test_screen_empty_sequence(self):
        result = self.screener.screen_sequence("")
        assert result["is_clean"] is True
        assert result["matches"] == []

    def test_screen_lowercase_sequence(self):
        seq = "atggagctgctggacttcgctatcgagctgctggacttcgct"
        result = self.screener.screen_sequence(seq)
        assert result["is_clean"] is False

    # --- calculate_risk_score ---
    def test_risk_score_clean_sequence(self):
        seq = "ATGCGTACGTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGC"
        score = self.screener.calculate_risk_score(seq)
        assert 0.0 <= score <= 1.0
        assert score < 0.3

    def test_risk_score_threat_sequence(self):
        seq = "ATGGAGCTGCTGGACTTCGCTATCGAGCTGCTGGACTTCGCTATCGAGCTGCTGGACTTC"
        score = self.screener.calculate_risk_score(seq)
        assert 0.0 <= score <= 1.0
        assert score > 0.5

    def test_risk_score_empty_sequence(self):
        score = self.screener.calculate_risk_score("")
        assert score == 0.0

    def test_risk_score_bounds(self):
        seq = "ATGGAGCTGCTGGACTTCGCTATCGAGCTGCTGGACTTCGCTATCGAGCTGCTGGACTTC"
        score = self.screener.calculate_risk_score(seq)
        assert 0.0 <= score <= 1.0

    # --- check_homology ---
    def test_homology_identical_sequences(self):
        seq = "ATGCGTACGTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGC"
        result = self.screener.check_homology(seq, seq)
        assert result["homology"] == 1.0
        assert result["is_homologous"] is True

    def test_homology_different_sequences(self):
        seq1 = "ATGCGTACGTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGC"
        seq2 = "TACGCATGCATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGAT"
        result = self.screener.check_homology(seq1, seq2)
        assert 0.0 <= result["homology"] <= 1.0
        assert result["homology"] < 0.5

    def test_homology_partial_match(self):
        seq1 = "ATGCGTACGTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGC"
        seq2 = "ATGCGTACGTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGT"
        result = self.screener.check_homology(seq1, seq2)
        assert 0.5 < result["homology"] <= 1.0

    def test_homology_empty_reference(self):
        seq = "ATGCGTACGTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGC"
        result = self.screener.check_homology(seq, "")
        assert result["homology"] == 0.0
        assert result["is_homologous"] is False


# ---------------------------------------------------------------------------
# DualUseDetector tests
# ---------------------------------------------------------------------------
class TestDualUseDetector:
    def setup_method(self):
        self.detector = DualUseDetector()

    # --- detect_dual_use ---
    def test_detect_dual_use_clean(self):
        seq = "ATGCGTACGTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGC"
        result = self.detector.detect_dual_use(seq)
        assert isinstance(result, dict)
        assert result["is_dual_use"] is False
        assert result["flags"] == []

    def test_detect_dual_use_virulence(self):
        seq = "ATGGCTATCGAGCTGCTGGACTTCGCTATCGAGCTGCTGGACTTCGCTATCGAGCTGCTG"
        result = self.detector.detect_dual_use(seq)
        assert result["is_dual_use"] is True
        assert len(result["flags"]) > 0

    def test_detect_dual_use_toxin(self):
        seq = "ATGTTCGCTGCTGCTGCTGCTGCTGCTGCTGCTGCTGCTGCTGCTGCTGCTGCTGCTGC"
        result = self.detector.detect_dual_use(seq)
        assert result["is_dual_use"] is True

    def test_detect_dual_use_empty(self):
        result = self.detector.detect_dual_use("")
        assert result["is_dual_use"] is False
        assert result["flags"] == []

    # --- classify_risk_level ---
    def test_classify_low(self):
        assert self.detector.classify_risk_level(0.1) == "Low"
        assert self.detector.classify_risk_level(0.2) == "Low"

    def test_classify_medium(self):
        assert self.detector.classify_risk_level(0.4) == "Medium"
        assert self.detector.classify_risk_level(0.5) == "Medium"

    def test_classify_high(self):
        assert self.detector.classify_risk_level(0.7) == "High"
        assert self.detector.classify_risk_level(0.8) == "High"

    def test_classify_extreme(self):
        assert self.detector.classify_risk_level(0.9) == "Extreme"
        assert self.detector.classify_risk_level(1.0) == "Extreme"

    def test_classify_boundary_values(self):
        assert self.detector.classify_risk_level(0.0) == "Low"
        assert self.detector.classify_risk_level(0.3) == "Medium"
        assert self.detector.classify_risk_level(0.6) == "High"
        assert self.detector.classify_risk_level(0.85) == "Extreme"


# ---------------------------------------------------------------------------
# ComplianceChecker tests
# ---------------------------------------------------------------------------
class TestComplianceChecker:
    def setup_method(self):
        self.checker = ComplianceChecker()

    # --- check_compliance ---
    def test_compliance_clean_sequence(self):
        seq = "ATGCGTACGTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGC"
        result = self.checker.check_compliance(seq, framework="NIH")
        assert isinstance(result, dict)
        assert result["compliant"] is True
        assert result["violations"] == []

    def test_compliance_threat_sequence(self):
        seq = "ATGGAGCTGCTGGACTTCGCTATCGAGCTGCTGGACTTCGCTATCGAGCTGCTGGACTTC"
        result = self.checker.check_compliance(seq, framework="NIH")
        assert result["compliant"] is False
        assert len(result["violations"]) > 0

    def test_compliance_different_frameworks(self):
        seq = "ATGCGTACGTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGC"
        for framework in ["NIH", "WHO", "CDC"]:
            result = self.checker.check_compliance(seq, framework=framework)
            assert result["compliant"] is True

    def test_compliance_empty_sequence(self):
        result = self.checker.check_compliance("", framework="NIH")
        assert result["compliant"] is True

    # --- generate_report ---
    def test_report_clean_sequence(self):
        seq = "ATGCGTACGTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGC"
        report = self.checker.generate_report(seq, framework="NIH")
        assert isinstance(report, dict)
        assert report["sequence_length"] == len(seq)
        assert report["framework"] == "NIH"
        assert report["compliant"] is True

    def test_report_threat_sequence(self):
        seq = "ATGGAGCTGCTGGACTTCGCTATCGAGCTGCTGGACTTCGCTATCGAGCTGCTGGACTTC"
        report = self.checker.generate_report(seq, framework="WHO")
        assert report["compliant"] is False
        assert len(report["violations"]) > 0

    def test_report_includes_risk_score(self):
        seq = "ATGCGTACGTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGC"
        report = self.checker.generate_report(seq, framework="CDC")
        assert "risk_score" in report
        assert 0.0 <= report["risk_score"] <= 1.0


# ---------------------------------------------------------------------------
# BiosecurityGate tests
# ---------------------------------------------------------------------------
class TestBiosecurityGate:
    def setup_method(self):
        self.gate = BiosecurityGate()

    # --- evaluate ---
    def test_evaluate_clean_sequence(self):
        seq = "ATGCGTACGTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGC"
        result = self.gate.evaluate(seq)
        assert isinstance(result, dict)
        assert result["passed"] is True
        assert result["risk_level"] == "Low"

    def test_evaluate_threat_sequence(self):
        seq = "ATGGAGCTGCTGGACTTCGCTATCGAGCTGCTGGACTTCGCTATCGAGCTGCTGGACTTC"
        result = self.gate.evaluate(seq)
        assert result["passed"] is False
        assert result["risk_level"] in ("High", "Extreme")

    def test_evaluate_empty_sequence(self):
        result = self.gate.evaluate("")
        assert result["passed"] is True

    def test_evaluate_includes_details(self):
        seq = "ATGCGTACGTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGC"
        result = self.gate.evaluate(seq)
        assert "risk_score" in result
        assert "screening_result" in result
        assert "dual_use_result" in result
        assert "compliance_result" in result

    def test_evaluate_borderline_sequence(self):
        seq = "ATGCGTACGTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGC"
        result = self.gate.evaluate(seq)
        assert result["passed"] is True
        assert result["risk_level"] in ("Low", "Medium")
