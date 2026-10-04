"""Test-driven development: MoClo assembly overhang design."""

from src.synbio.genetic_circuits import design_moclo_overhangs, validate_moclo_design


class TestDesignMoCloOverhangs:
    """Test design_moclo_overhangs assigns unique 4-bp overhangs."""

    def test_empty_list_returns_empty_dict(self):
        result = design_moclo_overhangs([])
        assert result == {}

    def test_four_parts_returns_four_overhangs(self):
        result = design_moclo_overhangs(["partA", "partB", "partC", "partD"])
        assert len(result) == 4

    def test_overhangs_are_4bp(self):
        result = design_moclo_overhangs(["partA", "partB", "partC", "partD"])
        for overhang in result.values():
            assert len(overhang) == 4

    def test_overhangs_have_valid_gc_content(self):
        result = design_moclo_overhangs(["partA", "partB", "partC", "partD"])
        for overhang in result.values():
            gc_count = overhang.count("G") + overhang.count("C")
            gc_content = gc_count / len(overhang)
            assert 0.4 <= gc_content <= 0.6

    def test_overhangs_are_unique(self):
        result = design_moclo_overhangs(["partA", "partB", "partC", "partD"])
        overhangs = list(result.values())
        assert len(overhangs) == len(set(overhangs))

    def test_no_palindromes(self):
        result = design_moclo_overhangs(["partA", "partB", "partC", "partD"])
        for overhang in result.values():
            assert overhang != overhang[::-1].translate(str.maketrans("ATGC", "TACG"))

    def test_no_reverse_complement_pairs(self):
        result = design_moclo_overhangs(["partA", "partB", "partC", "partD"])
        overhangs = list(result.values())
        for i in range(len(overhangs)):
            for j in range(i + 1, len(overhangs)):
                rc = overhangs[j][::-1].translate(str.maketrans("ATGC", "TACG"))
                assert overhangs[i] != rc


class TestValidateMoCloDesign:
    """Test validate_moclo_design checks overhang validity."""

    def test_valid_overhangs_returns_valid_true(self):
        overhangs = {
            "0": "AACC",
            "1": "AACG",
            "2": "ACAC",
            "3": "AGTC",
        }
        result = validate_moclo_design(overhangs)
        assert result["valid"] is True
        assert result["errors"] == []

    def test_duplicate_overhangs_returns_valid_false(self):
        overhangs = {
            "0": "AACC",
            "1": "AACC",
            "2": "ACAC",
            "3": "AGTC",
        }
        result = validate_moclo_design(overhangs)
        assert result["valid"] is False
        assert len(result["errors"]) > 0

    def test_palindrome_returns_valid_false(self):
        overhangs = {
            "0": "ATAT",
            "1": "AACC",
            "2": "ACAC",
            "3": "AGTC",
        }
        result = validate_moclo_design(overhangs)
        assert result["valid"] is False
        assert len(result["errors"]) > 0

    def test_reverse_complement_pair_returns_valid_false(self):
        overhangs = {
            "0": "AACC",
            "1": "GGTT",
            "2": "ACAC",
            "3": "AGTC",
        }
        result = validate_moclo_design(overhangs)
        assert result["valid"] is False
        assert len(result["errors"]) > 0

    def test_invalid_gc_content_returns_valid_false(self):
        overhangs = {
            "0": "AAAA",
            "1": "AACC",
            "2": "ACAC",
            "3": "AGTC",
        }
        result = validate_moclo_design(overhangs)
        assert result["valid"] is False
        assert len(result["errors"]) > 0

    def test_wrong_length_returns_valid_false(self):
        overhangs = {
            "0": "AACAA",
            "1": "AACC",
            "2": "ACAC",
            "3": "AGTC",
        }
        result = validate_moclo_design(overhangs)
        assert result["valid"] is False
        assert len(result["errors"]) > 0
