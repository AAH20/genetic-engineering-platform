"""TDD tests for async pipeline support and continue-on-error mode."""
import asyncio

from src.pipeline.pipeline import (
    AsyncPipelineStep,
    Pipeline,
    PipelineStep,
)


class TestAsyncPipelineStep:
    """Tests for AsyncPipelineStep class."""

    def test_async_step_with_async_function(self):
        """AsyncPipelineStep wraps an async function and executes it correctly."""
        async def async_double(x):
            return x * 2

        step = AsyncPipelineStep(name="async_double", func=async_double)
        result = asyncio.run(step.execute(5))
        assert result == 10

    def test_async_step_with_sync_function(self):
        """AsyncPipelineStep wraps a sync function and executes it correctly."""
        def sync_double(x):
            return x * 2

        step = AsyncPipelineStep(name="sync_double", func=sync_double)
        result = asyncio.run(step.execute(5))
        assert result == 10

    def test_async_step_with_context(self):
        """AsyncPipelineStep passes context to the function."""
        async def async_add_offset(x, ctx):
            return x + ctx.get("offset", 0)

        step = AsyncPipelineStep(name="add_offset", func=async_add_offset)
        result = asyncio.run(step.execute(5, context={"offset": 10}))
        assert result == 15

    def test_async_step_name(self):
        """AsyncPipelineStep stores the name correctly."""
        async def noop(x):
            return x

        step = AsyncPipelineStep(name="my_step", func=noop)
        assert step.name == "my_step"


class TestPipelineRunAsync:
    """Tests for Pipeline.run_async method."""

    def test_run_async_with_mixed_steps(self):
        """Pipeline.run_async handles both sync and async steps."""
        async def async_triple(x):
            return x * 3

        p = Pipeline("mixed")
        p.add_step(PipelineStep("sync_add", lambda x: x + 1))
        p.add_step(AsyncPipelineStep("async_triple", async_triple))
        p.add_step(PipelineStep("sync_sub", lambda x: x - 2))

        result = asyncio.run(p.run_async(5))
        # 5 + 1 = 6, 6 * 3 = 18, 18 - 2 = 16
        assert result.output == 16

    def test_run_async_returns_correct_output(self):
        """Pipeline.run_async returns the final output value."""
        async def async_identity(x):
            return x

        p = Pipeline("identity")
        p.add_step(AsyncPipelineStep("id", async_identity))
        result = asyncio.run(p.run_async(42))
        assert result.output == 42

    def test_run_async_with_context(self):
        """Pipeline.run_async passes context to all steps."""
        async def async_with_ctx(x, ctx):
            return x + ctx.get("bonus", 0)

        p = Pipeline("ctx_test")
        p.add_step(AsyncPipelineStep("step", async_with_ctx))
        result = asyncio.run(p.run_async(10, context={"bonus": 5}))
        assert result.output == 15

    def test_run_async_empty_pipeline(self):
        """Pipeline.run_async with no steps returns initial value."""
        p = Pipeline("empty")
        result = asyncio.run(p.run_async(99))
        assert result.output == 99

    def test_run_async_stops_on_error(self):
        """Pipeline.run_async stops on first error like run()."""
        async def async_fail(x):
            raise ValueError("async failure")

        p = Pipeline("error_test")
        p.add_step(PipelineStep("ok", lambda x: x + 1))
        p.add_step(AsyncPipelineStep("fail", async_fail))
        p.add_step(PipelineStep("never", lambda x: x * 100))

        result = asyncio.run(p.run_async(5))
        assert result.error is not None
        assert result.output is None
        assert result.steps_run == 1


class TestPipelineRunContinueOnError:
    """Tests for Pipeline.run_continue_on_error method."""

    def test_continue_on_error_continues_after_failure(self):
        """Pipeline continues executing steps after a step fails."""
        p = Pipeline("continue_test")
        p.add_step(PipelineStep("s1", lambda x: x + 1))
        p.add_step(PipelineStep("s2", lambda x: 1 / 0))  # fails
        p.add_step(PipelineStep("s3", lambda x: x * 10))

        result = p.run_continue_on_error(5)
        # s1: 5+1=6, s2: fails, s3: 6*10=60
        assert result.output == 60
        assert result.steps_run == 2

    def test_continue_on_error_collects_all_errors(self):
        """Pipeline collects all errors from failing steps."""
        p = Pipeline("multi_error")
        p.add_step(PipelineStep("s1", lambda x: 1 / 0))  # fails
        p.add_step(PipelineStep("s2", lambda x: x + 1))  # ok
        p.add_step(PipelineStep("s3", lambda x: 1 / 0))  # fails

        result = p.run_continue_on_error(5)
        assert len(result.errors) == 2
        assert result.steps_run == 1

    def test_continue_on_error_returns_partial_results(self):
        """Pipeline returns intermediate results from successful steps."""
        p = Pipeline("partial")
        p.add_step(PipelineStep("s1", lambda x: x + 1))  # 5+1=6
        p.add_step(PipelineStep("s2", lambda x: 1 / 0))  # fails
        p.add_step(PipelineStep("s3", lambda x: x * 2))  # 6*2=12

        result = p.run_continue_on_error(5)
        assert result.output == 12
        assert result.intermediate == [6, 12]

    def test_continue_on_error_no_errors(self):
        """Pipeline with no failures has empty errors list."""
        p = Pipeline("no_error")
        p.add_step(PipelineStep("s1", lambda x: x + 1))
        p.add_step(PipelineStep("s2", lambda x: x * 2))

        result = p.run_continue_on_error(5)
        assert result.errors == []
        assert result.output == 12
        assert result.steps_run == 2

    def test_continue_on_error_all_fail(self):
        """Pipeline where all steps fail returns None output."""
        p = Pipeline("all_fail")
        p.add_step(PipelineStep("s1", lambda x: 1 / 0))
        p.add_step(PipelineStep("s2", lambda x: 1 / 0))

        result = p.run_continue_on_error(5)
        assert result.output is None
        assert len(result.errors) == 2
        assert result.steps_run == 0
