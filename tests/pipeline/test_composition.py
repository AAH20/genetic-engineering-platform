"""TDD tests for pipeline composition: compose, split, and clone."""
import pytest

from src.pipeline.pipeline import Pipeline, PipelineStep


class TestCompose:
    def test_compose_with_empty_pipeline_returns_copy_of_original(self):
        p1 = Pipeline("p1")
        p1.add_step(PipelineStep("s1", lambda x: x + 1))
        p1.add_step(PipelineStep("s2", lambda x: x * 2))

        p2 = Pipeline("p2")
        result = p1.compose(p2)

        assert result is not p1
        assert len(result.steps) == 2
        assert result.steps[0].name == "s1"
        assert result.steps[1].name == "s2"

    def test_compose_with_non_empty_pipeline_appends_steps(self):
        p1 = Pipeline("p1")
        p1.add_step(PipelineStep("s1", lambda x: x + 1))

        p2 = Pipeline("p2")
        p2.add_step(PipelineStep("s2", lambda x: x * 2))
        p2.add_step(PipelineStep("s3", lambda x: x - 1))

        result = p1.compose(p2)

        assert len(result.steps) == 3
        assert result.steps[0].name == "s1"
        assert result.steps[1].name == "s2"
        assert result.steps[2].name == "s3"

    def test_compose_preserves_step_order(self):
        p1 = Pipeline("p1")
        p1.add_step(PipelineStep("a", lambda x: x + 1))
        p1.add_step(PipelineStep("b", lambda x: x + 2))

        p2 = Pipeline("p2")
        p2.add_step(PipelineStep("c", lambda x: x + 3))
        p2.add_step(PipelineStep("d", lambda x: x + 4))

        result = p1.compose(p2)

        names = [s.name for s in result.steps]
        assert names == ["a", "b", "c", "d"]

    def test_compose_does_not_modify_originals(self):
        p1 = Pipeline("p1")
        p1.add_step(PipelineStep("s1", lambda x: x + 1))

        p2 = Pipeline("p2")
        p2.add_step(PipelineStep("s2", lambda x: x * 2))

        _ = p1.compose(p2)

        assert len(p1.steps) == 1
        assert len(p2.steps) == 1


class TestSplit:
    def test_split_with_invalid_step_name_raises_value_error(self):
        p = Pipeline("p")
        p.add_step(PipelineStep("s1", lambda x: x + 1))
        p.add_step(PipelineStep("s2", lambda x: x * 2))

        with pytest.raises(ValueError, match="nonexistent"):
            p.split("nonexistent")

    def test_split_returns_correct_before_and_after_pipelines(self):
        p = Pipeline("p")
        p.add_step(PipelineStep("s1", lambda x: x + 1))
        p.add_step(PipelineStep("s2", lambda x: x * 2))
        p.add_step(PipelineStep("s3", lambda x: x - 1))

        before, after = p.split("s2")

        assert len(before.steps) == 1
        assert before.steps[0].name == "s1"
        assert len(after.steps) == 1
        assert after.steps[0].name == "s3"

    def test_split_at_first_step(self):
        p = Pipeline("p")
        p.add_step(PipelineStep("s1", lambda x: x + 1))
        p.add_step(PipelineStep("s2", lambda x: x * 2))

        before, after = p.split("s1")

        assert len(before.steps) == 0
        assert len(after.steps) == 1
        assert after.steps[0].name == "s2"

    def test_split_at_last_step(self):
        p = Pipeline("p")
        p.add_step(PipelineStep("s1", lambda x: x + 1))
        p.add_step(PipelineStep("s2", lambda x: x * 2))

        before, after = p.split("s2")

        assert len(before.steps) == 1
        assert before.steps[0].name == "s1"
        assert len(after.steps) == 0


class TestClone:
    def test_clone_creates_independent_copy(self):
        p = Pipeline("original")
        p.add_step(PipelineStep("s1", lambda x: x + 1))
        p.add_step(PipelineStep("s2", lambda x: x * 2))

        cloned = p.clone()

        assert cloned is not p
        assert cloned.name == p.name
        assert cloned.description == p.description
        assert len(cloned.steps) == len(p.steps)
        for orig_step, clone_step in zip(p.steps, cloned.steps):
            assert orig_step is not clone_step
            assert orig_step.name == clone_step.name

    def test_clone_modifications_do_not_affect_original(self):
        p = Pipeline("original")
        p.add_step(PipelineStep("s1", lambda x: x + 1))

        cloned = p.clone()
        cloned.add_step(PipelineStep("s2", lambda x: x * 2))

        assert len(p.steps) == 1
        assert len(cloned.steps) == 2

    def test_clone_preserves_step_data(self):
        p = Pipeline("original", description="test pipeline")
        p.add_step(PipelineStep("s1", lambda x: x + 1, metadata={"key": "value"}))

        cloned = p.clone()

        assert cloned.name == "original"
        assert cloned.description == "test pipeline"
        assert cloned.steps[0].name == "s1"
        assert cloned.steps[0].metadata == {"key": "value"}
