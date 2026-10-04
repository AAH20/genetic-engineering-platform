"""TDD tests for conditional branching in pipeline module."""
from src.pipeline.pipeline import (
    ConditionalStep,
    Pipeline,
    PipelineStep,
)


class TestConditionalStep:
    def test_true_predicate_runs_if_true(self):
        step = ConditionalStep(
            predicate=lambda v, ctx: v > 0,
            if_true=PipelineStep("pos", lambda v: "positive"),
            if_false=PipelineStep("neg", lambda v: "negative"),
        )
        result = step.execute(5)
        assert result == "positive"

    def test_false_predicate_runs_if_false(self):
        step = ConditionalStep(
            predicate=lambda v, ctx: v > 0,
            if_true=PipelineStep("pos", lambda v: "positive"),
            if_false=PipelineStep("neg", lambda v: "negative"),
        )
        result = step.execute(-3)
        assert result == "negative"

    def test_predicate_receives_value_and_context(self):
        received = {}

        def pred(v, ctx):
            received["value"] = v
            received["context"] = ctx
            return True

        step = ConditionalStep(
            predicate=pred,
            if_true=PipelineStep("t", lambda v: "yes"),
            if_false=PipelineStep("f", lambda v: "no"),
        )
        step.execute(42, context={"key": "val"})
        assert received["value"] == 42
        assert received["context"] == {"key": "val"}


class TestPipelineAddConditionalStep:
    def test_add_conditional_step(self):
        p = Pipeline("test")
        p.add_conditional_step(
            predicate=lambda v, ctx: v > 0,
            if_true=PipelineStep("pos", lambda v: "positive"),
            if_false=PipelineStep("neg", lambda v: "negative"),
        )
        assert len(p.steps) == 1
        assert isinstance(p.steps[0], ConditionalStep)

    def test_run_with_conditional_step_true_branch(self):
        p = Pipeline("test")
        p.add_conditional_step(
            predicate=lambda v, ctx: v > 0,
            if_true=PipelineStep("pos", lambda v: v * 10),
            if_false=PipelineStep("neg", lambda v: v - 100),
        )
        result = p.run(5)
        assert result.output == 50
        assert result.error is None

    def test_run_with_conditional_step_false_branch(self):
        p = Pipeline("test")
        p.add_conditional_step(
            predicate=lambda v, ctx: v > 0,
            if_true=PipelineStep("pos", lambda v: v * 10),
            if_false=PipelineStep("neg", lambda v: v - 100),
        )
        result = p.run(-5)
        assert result.output == -105
        assert result.error is None

    def test_run_conditional_chained_with_regular_steps(self):
        p = Pipeline("test")
        p.add_step(PipelineStep("add", lambda v: v + 1))
        p.add_conditional_step(
            predicate=lambda v, ctx: v > 5,
            if_true=PipelineStep("big", lambda v: v * 2),
            if_false=PipelineStep("small", lambda v: v * 3),
        )
        result = p.run(4)
        assert result.output == 15  # (4+1)*3
        assert result.steps_run == 2
