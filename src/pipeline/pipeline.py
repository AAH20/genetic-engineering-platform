"""Unified pipeline module for composing multi-step workflows.

Provides a declarative way to chain processing steps with error handling,
context propagation, and intermediate result tracing.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Optional


@dataclass
class PipelineStep:
    """A single processing step in a pipeline.

    Attributes:
        name: Human-readable step identifier.
        func: Callable that transforms the input (and optionally context).
        metadata: Arbitrary key-value metadata for the step.
    """

    name: str
    func: Callable[..., Any]
    metadata: dict[str, Any] = field(default_factory=dict)

    def execute(self, value: Any, context: dict[str, Any] | None = None) -> Any:
        """Execute the step, passing context if the function accepts it."""
        import inspect
        sig = inspect.signature(self.func)
        params = list(sig.parameters.keys())
        if len(params) >= 2:
            return self.func(value, context)
        return self.func(value)


@dataclass
class PipelineResult:
    """Result of running a pipeline.

    Attributes:
        output: Final output value (None if pipeline errored).
        steps_run: Number of steps successfully executed.
        intermediate: List of intermediate values after each step.
        error: Error message if pipeline failed, None otherwise.
    """

    output: Any = None
    steps_run: int = 0
    intermediate: list[Any] = field(default_factory=list)
    error: Optional[str] = None


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
        self.steps: list[PipelineStep] = []

    def add_step(self, step: PipelineStep) -> Pipeline:
        """Add a step and return self for chaining."""
        self.steps.append(step)
        return self

    def run(self, initial_value: Any, context: dict[str, Any] | None = None) -> PipelineResult:
        """Execute all steps in order, threading output through.

        Stops on first error and returns the error in PipelineResult.
        """
        value = initial_value
        intermediate: list[Any] = []
        steps_run = 0

        for step in self.steps:
            try:
                value = step.execute(value, context)
                intermediate.append(value)
                steps_run += 1
            except Exception as exc:
                return PipelineResult(
                    output=None,
                    steps_run=steps_run,
                    intermediate=intermediate,
                    error=f"{step.name}: {exc}",
                )

        return PipelineResult(
            output=value,
            steps_run=steps_run,
            intermediate=intermediate,
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
