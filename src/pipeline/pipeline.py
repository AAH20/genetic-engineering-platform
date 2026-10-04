"""Unified pipeline module for composing multi-step workflows.

Provides a declarative way to chain processing steps with error handling,
context propagation, and intermediate result tracing.
"""

from __future__ import annotations

import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from typing import Any, Callable, Optional


@dataclass
class PipelineStep:
    """A single processing step in a pipeline.

    Attributes:
        name: Human-readable step identifier.
        func: Callable that transforms the input (and optionally context).
        metadata: Arbitrary key-value metadata for the step.
        retry_count: Number of times to retry on failure (default 0).
        retry_delay: Seconds to wait between retries (default 0.0).
    """

    name: str
    func: Callable[..., Any]
    metadata: dict[str, Any] = field(default_factory=dict)
    retry_count: int = 0
    retry_delay: float = 0.0
    retries_used: int = 0

    def execute(self, value: Any, context: dict[str, Any] | None = None) -> Any:
        """Execute the step with retry logic, passing context if the function accepts it."""
        import inspect
        sig = inspect.signature(self.func)
        params = list(sig.parameters.keys())
        self.retries_used = 0
        for attempt in range(self.retry_count + 1):
            try:
                if len(params) >= 2:
                    return self.func(value, context)
                return self.func(value)
            except Exception:
                if attempt < self.retry_count:
                    self.retries_used += 1
                    if self.retry_delay > 0:
                        time.sleep(self.retry_delay)
                else:
                    raise
        return None  # unreachable


@dataclass
class ConditionalStep(PipelineStep):
    """A step that branches based on a predicate.

    Attributes:
        predicate: Callable(value, context) -> bool that selects the branch.
        if_true: PipelineStep executed when predicate returns True.
        if_false: PipelineStep executed when predicate returns False.
    """

    name: str = "conditional"
    func: Callable[..., Any] = field(default=lambda v, ctx: None)
    predicate: Callable[..., bool] = field(default=lambda v, ctx: True)
    if_true: Optional[PipelineStep] = None
    if_false: Optional[PipelineStep] = None

    def __post_init__(self) -> None:
        self.func = lambda v, ctx: self._branch(v, ctx)

    def _branch(self, value: Any, context: dict[str, Any] | None = None) -> Any:
        if self.predicate(value, context):
            return self.if_true.execute(value, context)
        return self.if_false.execute(value, context)

    def execute(self, value: Any, context: dict[str, Any] | None = None) -> Any:
        """Evaluate predicate and run the appropriate branch."""
        return self._branch(value, context)


@dataclass
class ParallelStep:
    """A step that runs multiple PipelineSteps concurrently.

    Attributes:
        name: Human-readable step identifier.
        steps: List of PipelineStep to execute in parallel.
    """

    name: str
    steps: list[PipelineStep]

    def execute(self, value: Any, context: dict[str, Any] | None = None) -> list[Any]:
        """Execute all steps in parallel using ThreadPoolExecutor.

        Returns:
            List of results from each step, in the same order as the input steps.
        """
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(step.execute, value, context)
                for step in self.steps
            ]
            return [f.result() for f in futures]


@dataclass
class PipelineResult:
    """Result of running a pipeline.

    Attributes:
        output: Final output value (None if pipeline errored).
        steps_run: Number of steps successfully executed.
        intermediate: List of intermediate values after each step.
        error: Error message if pipeline failed, None otherwise.
        retries_used: Dict mapping step name to number of retries used.
    """

    output: Any = None
    steps_run: int = 0
    intermediate: list[Any] = field(default_factory=list)
    error: Optional[str] = None
    retries_used: dict[str, int] = field(default_factory=dict)


class Pipeline:
    """A composable pipeline of processing steps.

    Usage:
        p = Pipeline("my_pipeline")
        p.add_step(PipelineStep("double", lambda x: x * 2))
        result = p.run(5)
        assert result.output == 10
    """

    def __init__(self, name: str, description: str = "") -> None:
        self.name = name
        self.description = description
        self.steps: list[Any] = []

    def add_step(self, step: PipelineStep) -> Pipeline:
        """Add a step and return self for chaining."""
        self.steps.append(step)
        return self

    def add_conditional_step(
        self,
        predicate: Callable[..., bool],
        if_true: PipelineStep,
        if_false: PipelineStep,
    ) -> Pipeline:
        """Add a conditional branching step and return self for chaining."""
        self.steps.append(
            ConditionalStep(
                name="conditional",
                predicate=predicate,
                if_true=if_true,
                if_false=if_false,
            )
        )
        return self

    def add_parallel_step(self, step: ParallelStep) -> Pipeline:
        """Add a parallel step and return self for chaining."""
        self.steps.append(step)
        return self

    def run(self, initial_value: Any, context: dict[str, Any] | None = None) -> PipelineResult:
        """Execute all steps in order, threading output through.

        Stops on first error and returns the error in PipelineResult.
        """
        value = initial_value
        intermediate: list[Any] = []
        steps_run = 0
        retries_used: dict[str, int] = {}

        for step in self.steps:
            try:
                value = step.execute(value, context)
                intermediate.append(value)
                steps_run += 1
                retries_used[step.name] = getattr(step, "retries_used", 0)
            except Exception as exc:
                retries_used[step.name] = getattr(step, "retries_used", 0)
                return PipelineResult(
                    output=None,
                    steps_run=steps_run,
                    intermediate=intermediate,
                    error=f"{step.name}: {exc}",
                    retries_used=retries_used,
                )

        return PipelineResult(
            output=value,
            steps_run=steps_run,
            intermediate=intermediate,
            retries_used=retries_used,
        )


def run_pipeline(
    steps: list[PipelineStep],
    initial_value: Any,
    context: dict[str, Any] | None = None,
) -> PipelineResult:
    """Convenience function: build a pipeline from steps and run it."""
    p = Pipeline("anonymous")
    for step in steps:
        p.add_step(step)
    return p.run(initial_value, context)
