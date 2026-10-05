"""TDD tests for dynamic step manipulation in Pipeline."""
import pytest

from src.pipeline.pipeline import Pipeline, PipelineStep


class TestInsertStep:
    def test_insert_step_at_correct_index(self):
        p = Pipeline("test")
        p.add_step(PipelineStep("s1", lambda x: x + 1))
        p.add_step(PipelineStep("s3", lambda x: x * 3))
        p.insert_step(PipelineStep("s2", lambda x: x * 2), index=1)
        assert [s.name for s in p.steps] == ["s1", "s2", "s3"]

    def test_insert_step_at_beginning(self):
        p = Pipeline("test")
        p.add_step(PipelineStep("s2", lambda x: x * 2))
        p.insert_step(PipelineStep("s1", lambda x: x + 1), index=0)
        assert [s.name for s in p.steps] == ["s1", "s2"]

    def test_insert_step_at_end(self):
        p = Pipeline("test")
        p.add_step(PipelineStep("s1", lambda x: x + 1))
        p.insert_step(PipelineStep("s2", lambda x: x * 2), index=1)
        assert [s.name for s in p.steps] == ["s1", "s2"]

    def test_insert_step_returns_self_for_chaining(self):
        p = Pipeline("test")
        result = p.insert_step(PipelineStep("s1", lambda x: x + 1), index=0)
        assert result is p

    def test_insert_step_invalid_index_raises_index_error(self):
        p = Pipeline("test")
        p.add_step(PipelineStep("s1", lambda x: x + 1))
        with pytest.raises(IndexError):
            p.insert_step(PipelineStep("s2", lambda x: x * 2), index=5)

    def test_insert_step_negative_index_raises_index_error(self):
        p = Pipeline("test")
        p.add_step(PipelineStep("s1", lambda x: x + 1))
        with pytest.raises(IndexError):
            p.insert_step(PipelineStep("s2", lambda x: x * 2), index=-1)


class TestRemoveStep:
    def test_remove_step_removes_correct_step(self):
        p = Pipeline("test")
        p.add_step(PipelineStep("s1", lambda x: x + 1))
        p.add_step(PipelineStep("s2", lambda x: x * 2))
        p.add_step(PipelineStep("s3", lambda x: x * 3))
        p.remove_step("s2")
        assert [s.name for s in p.steps] == ["s1", "s3"]

    def test_remove_step_returns_self_for_chaining(self):
        p = Pipeline("test")
        p.add_step(PipelineStep("s1", lambda x: x + 1))
        result = p.remove_step("s1")
        assert result is p

    def test_remove_step_invalid_name_raises_value_error(self):
        p = Pipeline("test")
        p.add_step(PipelineStep("s1", lambda x: x + 1))
        with pytest.raises(ValueError):
            p.remove_step("nonexistent")


class TestReplaceStep:
    def test_replace_step_replaces_correct_step(self):
        p = Pipeline("test")
        p.add_step(PipelineStep("s1", lambda x: x + 1))
        p.add_step(PipelineStep("s2", lambda x: x * 2))
        p.replace_step("s1", PipelineStep("s1_new", lambda x: x * 10))
        assert [s.name for s in p.steps] == ["s1_new", "s2"]

    def test_replace_step_returns_self_for_chaining(self):
        p = Pipeline("test")
        p.add_step(PipelineStep("s1", lambda x: x + 1))
        result = p.replace_step("s1", PipelineStep("s1_new", lambda x: x * 10))
        assert result is p

    def test_replace_step_invalid_name_raises_value_error(self):
        p = Pipeline("test")
        p.add_step(PipelineStep("s1", lambda x: x + 1))
        with pytest.raises(ValueError):
            p.replace_step("nonexistent", PipelineStep("new", lambda x: x))


class TestGetStep:
    def test_get_step_returns_correct_step(self):
        p = Pipeline("test")
        step1 = PipelineStep("s1", lambda x: x + 1)
        step2 = PipelineStep("s2", lambda x: x * 2)
        p.add_step(step1)
        p.add_step(step2)
        assert p.get_step("s1") is step1
        assert p.get_step("s2") is step2

    def test_get_step_invalid_name_raises_value_error(self):
        p = Pipeline("test")
        p.add_step(PipelineStep("s1", lambda x: x + 1))
        with pytest.raises(ValueError):
            p.get_step("nonexistent")
