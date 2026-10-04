"""TDD tests for parallel step execution in pipeline module."""
from src.pipeline.pipeline import (
    ParallelStep,
    Pipeline,
    PipelineStep,
)


class TestParallelStep:
    def test_empty_list_returns_empty(self):
        step = ParallelStep(name="empty_parallel", steps=[])
        result = step.execute(42)
        assert result == []

    def test_single_step_returns_list_of_one(self):
        step = ParallelStep(
            name="single",
            steps=[PipelineStep("s1", lambda x: x * 2)],
        )
        result = step.execute(5)
        assert result == [10]

    def test_multiple_steps_returns_all_results(self):
        step = ParallelStep(
            name="multi",
            steps=[
                PipelineStep("s1", lambda x: x + 1),
                PipelineStep("s2", lambda x: x * 2),
                PipelineStep("s3", lambda x: x - 3),
            ],
        )
        result = step.execute(5)
        assert len(result) == 3
        assert result == [6, 10, 2]

    def test_results_are_correct(self):
        step = ParallelStep(
            name="correct",
            steps=[
                PipelineStep("double", lambda x: x * 2),
                PipelineStep("triple", lambda x: x * 3),
            ],
        )
        result = step.execute(7)
        assert result == [14, 21]

    def test_with_context(self):
        step = ParallelStep(
            name="ctx",
            steps=[
                PipelineStep("add_offset", lambda x, ctx: x + ctx.get("offset", 0)),
                PipelineStep("mul_factor", lambda x, ctx: x * ctx.get("factor", 1)),
            ],
        )
        result = step.execute(5, context={"offset": 10, "factor": 3})
        assert result == [15, 15]


class TestPipelineAddParallelStep:
    def test_add_parallel_step(self):
        p = Pipeline("test")
        parallel = ParallelStep(
            name="par",
            steps=[PipelineStep("s1", lambda x: x + 1)],
        )
        p.add_parallel_step(parallel)
        assert len(p.steps) == 1
        assert p.steps[0] is parallel

    def test_run_with_parallel_step(self):
        p = Pipeline("test")
        p.add_step(PipelineStep("init", lambda x: x + 1))
        p.add_parallel_step(
            ParallelStep(
                name="par",
                steps=[
                    PipelineStep("double", lambda x: x * 2),
                    PipelineStep("triple", lambda x: x * 3),
                ],
            )
        )
        result = p.run(5)
        assert result.output == [12, 18]
        assert result.steps_run == 2
        assert result.error is None

    def test_run_parallel_then_sequential(self):
        p = Pipeline("test")
        p.add_parallel_step(
            ParallelStep(
                name="par",
                steps=[
                    PipelineStep("a", lambda x: x + 10),
                    PipelineStep("b", lambda x: x + 20),
                ],
            )
        )
        p.add_step(PipelineStep("final", lambda x: sum(x)))
        result = p.run(5)
        assert result.output == 40
        assert result.steps_run == 2
