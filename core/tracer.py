from typing import Any, Generator


def collect_steps(gen: Generator[dict[str, Any], None, None]) -> list[dict[str, Any]]:
    """Consume a traced algorithm generator, return all steps."""
    return list(gen)


def get_step(steps: list[dict[str, Any]], index: int) -> dict[str, Any]:
    """Get a specific step, clamped to valid range."""
    if not steps:
        return {}
    return steps[max(0, min(index, len(steps) - 1))]
