"""Tests for BiosecurityGate audit trail logging."""
import hashlib

from src.biosecurity.screening import BiosecurityGate


class TestAuditTrail:
    def setup_method(self):
        self.gate = BiosecurityGate()

    def test_audit_log_starts_empty(self):
        assert self.gate._audit_log == []

    def test_evaluate_adds_entry_to_log(self):
        seq = "ATGCGTACGTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGC"
        self.gate.evaluate(seq)
        assert len(self.gate._audit_log) == 1

    def test_audit_entry_has_required_fields(self):
        seq = "ATGCGTACGTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGC"
        self.gate.evaluate(seq)
        entry = self.gate._audit_log[0]
        assert "timestamp" in entry
        assert "sequence_hash" in entry
        assert "result" in entry
        assert "framework" in entry

    def test_audit_entry_result_passed(self):
        seq = "ATGCGTACGTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGC"
        self.gate.evaluate(seq)
        entry = self.gate._audit_log[0]
        assert entry["result"] == "passed"

    def test_audit_entry_result_failed(self):
        seq = "ATGGAGCTGCTGGACTTCGCTATCGAGCTGCTGGACTTCGCTATCGAGCTGCTGGACTTC"
        self.gate.evaluate(seq)
        entry = self.gate._audit_log[0]
        assert entry["result"] == "failed"

    def test_audit_entry_framework_default(self):
        seq = "ATGCGTACGTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGC"
        self.gate.evaluate(seq)
        entry = self.gate._audit_log[0]
        assert entry["framework"] == "NIH"

    def test_audit_entry_framework_custom(self):
        seq = "ATGCGTACGTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGC"
        self.gate.evaluate(seq, framework="WHO")
        entry = self.gate._audit_log[0]
        assert entry["framework"] == "WHO"

    def test_audit_entry_timestamp_is_iso_format(self):
        seq = "ATGCGTACGTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGC"
        self.gate.evaluate(seq)
        entry = self.gate._audit_log[0]
        # ISO format: YYYY-MM-DDTHH:MM:SS.ffffff
        assert "T" in entry["timestamp"]
        parts = entry["timestamp"].split("T")
        assert len(parts) == 2
        date_parts = parts[0].split("-")
        assert len(date_parts) == 3

    def test_audit_entry_sequence_hash_is_sha256(self):
        seq = "ATGCGTACGTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGC"
        self.gate.evaluate(seq)
        entry = self.gate._audit_log[0]
        expected_hash = hashlib.sha256(seq.encode()).hexdigest()
        assert entry["sequence_hash"] == expected_hash

    def test_audit_entry_sequence_hash_differs_per_sequence(self):
        seq1 = "ATGCGTACGTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGC"
        seq2 = "ATGGAGCTGCTGGACTTCGCTATCGAGCTGCTGGACTTCGCTATCGAGCTGCTGGACTTC"
        self.gate.evaluate(seq1)
        self.gate.evaluate(seq2)
        hash1 = self.gate._audit_log[0]["sequence_hash"]
        hash2 = self.gate._audit_log[1]["sequence_hash"]
        assert hash1 != hash2

    def test_get_audit_log_returns_all_entries(self):
        seq1 = "ATGCGTACGTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGC"
        seq2 = "ATGGAGCTGCTGGACTTCGCTATCGAGCTGCTGGACTTCGCTATCGAGCTGCTGGACTTC"
        self.gate.evaluate(seq1)
        self.gate.evaluate(seq2)
        log = self.gate.get_audit_log()
        assert len(log) == 2
        assert log[0]["sequence_hash"] != log[1]["sequence_hash"]

    def test_clear_audit_log_empties_log(self):
        seq = "ATGCGTACGTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGC"
        self.gate.evaluate(seq)
        assert len(self.gate._audit_log) == 1
        self.gate.clear_audit_log()
        assert self.gate._audit_log == []

    def test_clear_audit_log_allows_new_entries(self):
        seq = "ATGCGTACGTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGC"
        self.gate.evaluate(seq)
        self.gate.clear_audit_log()
        self.gate.evaluate(seq)
        assert len(self.gate._audit_log) == 1

    def test_multiple_evaluates_accumulate_entries(self):
        seq = "ATGCGTACGTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGC"
        self.gate.evaluate(seq)
        self.gate.evaluate(seq)
        self.gate.evaluate(seq)
        assert len(self.gate._audit_log) == 3
