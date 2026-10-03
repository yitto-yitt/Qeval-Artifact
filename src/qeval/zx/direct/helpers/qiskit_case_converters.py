from __future__ import annotations

import copy
from typing import Any


SUPPORTED_FRAMEWORKS = {"qiskit"}


def convert_kwargs_for_framework(kwargs: dict[str, Any], framework: str, task_id: int) -> dict[str, Any]:
    return {
        key: convert_value_for_framework(value, framework, task_id)
        for key, value in kwargs.items()
    }


def convert_args_for_framework(args: tuple[Any, ...], framework: str, task_id: int) -> tuple[Any, ...]:
    return tuple(convert_value_for_framework(value, framework, task_id) for value in args)


def convert_value_for_framework(value: Any, framework: str, task_id: int) -> Any:
    normalized = (framework or "qiskit").strip().lower()
    if normalized not in SUPPORTED_FRAMEWORKS:
        raise NotImplementedError(
            "This clean ZX experiment folder only supports qiskit self-verification inputs. "
            f"Unsupported framework={framework!r} for task_id={task_id}."
        )
    return clone_value(value)


def clone_value(value: Any) -> Any:
    try:
        return copy.deepcopy(value)
    except Exception:
        if isinstance(value, dict):
            return {key: clone_value(item) for key, item in value.items()}
        if isinstance(value, list):
            return [clone_value(item) for item in value]
        if isinstance(value, tuple):
            return tuple(clone_value(item) for item in value)
        if isinstance(value, set):
            return {clone_value(item) for item in value}
        return value
