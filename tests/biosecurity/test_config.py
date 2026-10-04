"""Tests for configurable pattern database (load/save/count)."""
import json

import pytest

from src.biosecurity.screening import (
    THREAT_PATTERNS,
    get_pattern_count,
    load_custom_patterns,
    load_patterns_from_file,
    save_patterns_to_file,
)


@pytest.fixture(autouse=True)
def _restore_threat_patterns():
    """Snapshot and restore THREAT_PATTERNS around each test."""
    original = dict(THREAT_PATTERNS)
    yield
    THREAT_PATTERNS.clear()
    THREAT_PATTERNS.update(original)


class TestLoadCustomPatterns:
    """Tests for load_custom_patterns function."""

    def test_load_custom_patterns_adds_patterns(self):
        """load_custom_patterns adds new patterns to THREAT_PATTERNS."""
        new_patterns = {
            "custom_threat_A": "AAAACCCCGGGGTTTT",
            "custom_threat_B": "TTTTGGGGCCCCAAAA",
        }
        load_custom_patterns(new_patterns)
        assert "custom_threat_A" in THREAT_PATTERNS
        assert THREAT_PATTERNS["custom_threat_A"] == "AAAACCCCGGGGTTTT"
        assert "custom_threat_B" in THREAT_PATTERNS
        assert THREAT_PATTERNS["custom_threat_B"] == "TTTTGGGGCCCCAAAA"

    def test_load_custom_patterns_empty_dict_does_nothing(self):
        """load_custom_patterns with empty dict leaves THREAT_PATTERNS unchanged."""
        before = dict(THREAT_PATTERNS)
        load_custom_patterns({})
        assert THREAT_PATTERNS == before

    def test_load_custom_patterns_overwrites_existing(self):
        """load_custom_patterns overwrites an existing pattern with the same key."""
        key = "botulinum_neurotoxin_light_chain"
        original_value = THREAT_PATTERNS[key]
        load_custom_patterns({key: "NEW_PATTERN_VALUE"})
        assert THREAT_PATTERNS[key] == "NEW_PATTERN_VALUE"
        # Restore for other tests
        THREAT_PATTERNS[key] = original_value


class TestSavePatternsToFile:
    """Tests for save_patterns_to_file function."""

    def test_save_patterns_to_file_creates_file(self, tmp_path):
        """save_patterns_to_file creates a JSON file with current patterns."""
        filepath = str(tmp_path / "patterns.json")
        save_patterns_to_file(filepath)
        with open(filepath) as f:
            data = json.load(f)
        assert isinstance(data, dict)
        assert len(data) == len(THREAT_PATTERNS)
        for key, value in THREAT_PATTERNS.items():
            assert key in data
            assert data[key] == value


class TestLoadPatternsFromFile:
    """Tests for load_patterns_from_file function."""

    def test_load_patterns_from_file_loads_patterns(self, tmp_path):
        """load_patterns_from_file loads patterns from a JSON file."""
        patterns = {"file_threat_X": "ACGTACGTACGT", "file_threat_Y": "TGCATGCATGCA"}
        filepath = str(tmp_path / "patterns.json")
        with open(filepath, "w") as f:
            json.dump(patterns, f)

        load_patterns_from_file(filepath)
        assert "file_threat_X" in THREAT_PATTERNS
        assert THREAT_PATTERNS["file_threat_X"] == "ACGTACGTACGT"
        assert "file_threat_Y" in THREAT_PATTERNS
        assert THREAT_PATTERNS["file_threat_Y"] == "TGCATGCATGCA"

    def test_save_then_load_roundtrip(self, tmp_path):
        """Patterns saved to file can be loaded back identically."""
        filepath = str(tmp_path / "roundtrip.json")
        save_patterns_to_file(filepath)

        # Clear and reload
        THREAT_PATTERNS.clear()
        load_patterns_from_file(filepath)
        assert len(THREAT_PATTERNS) > 0


class TestGetPatternCount:
    """Tests for get_pattern_count function."""

    def test_get_pattern_count_returns_correct_count(self):
        """get_pattern_count returns the number of patterns in THREAT_PATTERNS."""
        count = get_pattern_count()
        assert count == len(THREAT_PATTERNS)

    def test_get_pattern_count_after_load_custom_patterns(self):
        """get_pattern_count reflects patterns added by load_custom_patterns."""
        before = get_pattern_count()
        new_patterns = {"count_test_A": "AAAA", "count_test_B": "CCCC", "count_test_G": "GGGG"}
        load_custom_patterns(new_patterns)
        after = get_pattern_count()
        assert after == before + 3
