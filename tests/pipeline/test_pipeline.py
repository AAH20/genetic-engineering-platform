"""TDD tests for unified pipeline module."""
from src.pipeline.pipeline import (
    Pipeline,
    PipelineResult,
    PipelineStep,
    run_pipeline,
)


class TestPipelineStep:
    def test_step_init(self):
        step = PipelineStep(name="test", func=lambda x: x * 2)
        assert step.name == "test"
        assert step.func(5) == 10

    def test_step_with_metadata(self):
        step = PipelineStep(
            name="test",
            func=lambda x: x,
            metadata={"author": "test"},
        )
        assert step.metadata["author"] == "test"


class TestPipeline:
    def test_add_step(self):
        p = Pipeline("test")
        p.add_step(PipelineStep("s1", lambda x: x + 1))
        assert len(p.steps) == 1

    def test_run_single_step(self):
        p = Pipeline("test")
        p.add_step(PipelineStep("s1", lambda x: x * 2))
        result = p.run(5)
        assert result.output == 10

    def test_run_chained_steps(self):
        p = Pipeline("test")
        p.add_step(PipelineStep("s1", lambda x: x + 1))
        p.add_step(PipelineStep("s2", lambda x: x * 3))
        result = p.run(5)
        assert result.output == 18

    def test_run_with_context(self):
        p = Pipeline("test")
        p.add_step(PipelineStep("s1", lambda x, ctx: x + ctx.get("offset", 0)))
        result = p.run(5, context={"offset": 10})
        assert result.output == 15

    def test_run_empty_pipeline(self):
        p = Pipeline("empty")
        result = p.run(42)
        assert result.output == 42

    def test_run_stops_on_error(self):
        p = Pipeline("error_test")
        p.add_step(PipelineStep("s1", lambda x: x + 1))
        p.add_step(PipelineStep("s2", lambda x: 1 / 0))
        result = p.run(5)
        assert result.error is not None
        assert result.output is None

    def test_run_records_intermediate(self):
        p = Pipeline("trace")
        p.add_step(PipelineStep("s1", lambda x: x + 1))
        p.add_step(PipelineStep("s2", lambda x: x * 2))
        result = p.run(5)
        assert len(result.intermediate) == 2
        assert result.intermediate[0] == 6
        assert result.intermediate[1] == 12

    def test_pipeline_name(self):
        p = Pipeline("my_pipeline")
        assert p.name == "my_pipeline"

    def test_pipeline_description(self):
        p = Pipeline("test", description="A test pipeline")
        assert p.description == "A test pipeline"


class TestPipelineResult:
    def test_result_success(self):
        r = PipelineResult(output=42, steps_run=2)
        assert r.output == 42
        assert r.steps_run == 2
        assert r.error is None

    def test_result_with_error(self):
        r = PipelineResult(output=None, steps_run=1, error="fail")
        assert r.error == "fail"
        assert r.output is None

    def test_result_intermediate(self):
        r = PipelineResult(output=10, steps_run=3, intermediate=[5, 8, 10])
        assert r.intermediate == [5, 8, 10]


class TestRunPipeline:
    def test_run_pipeline_function(self):
        steps = [
            PipelineStep("s1", lambda x: x + 1),
            PipelineStep("s2", lambda x: x * 2),
        ]
        result = run_pipeline(steps, 5)
        assert result.output == 12

    def test_run_pipeline_with_error(self):
        steps = [
            PipelineStep("s1", lambda x: x + 1),
            PipelineStep("s2", lambda x: 1 / 0),
        ]
        result = run_pipeline(steps, 5)
        assert result.error is not None
