from __future__ import annotations

from dataclasses import dataclass
from typing import Any


TARGET_QISKIT_VERSIONS = {
    "qiskit": "2.3.1",
    "qiskit-aer": "0.17.2",
    "qiskit-ibm-runtime": "0.46.1",
}

CLASS_ID = 2
TASK_IDS = [2, 3, 5, 6, 11, 39, 62, 66, 139]


@dataclass(frozen=True)
class TaskSpec:
    task_id: int
    class_id: int
    difficulty: str
    entrypoint: str
    signature: str
    description: str
    return_format: str


TASK_SPECS: dict[int, TaskSpec] = {
    2: TaskSpec(
        task_id=2,
        class_id=CLASS_ID,
        difficulty="basic",
        entrypoint="create_bell_statevector",
        signature="create_bell_statevector()",
        description="Return a Phi+ Bell statevector.",
        return_format="Return only the resulting Statevector object.",
    ),
    3: TaskSpec(
        task_id=3,
        class_id=CLASS_ID,
        difficulty="basic",
        entrypoint="create_ghz",
        signature="create_ghz(drawing=False)",
        description=(
            "Generate a QuantumCircuit for a 3-qubit GHZ state and measure it. "
            "If drawing is True, return both the circuit object and the Matplotlib drawing; "
            "otherwise return only the circuit object."
        ),
        return_format="Return a measured QuantumCircuit when drawing is False.",
    ),
    5: TaskSpec(
        task_id=5,
        class_id=CLASS_ID,
        difficulty="basic",
        entrypoint="create_state_prep",
        signature="create_state_prep()",
        description='Return a 2-qubit QuantumCircuit that prepares the bitstring state "01".',
        return_format="Return only the resulting QuantumCircuit.",
    ),
    6: TaskSpec(
        task_id=6,
        class_id=CLASS_ID,
        difficulty="basic",
        entrypoint="create_state_prep",
        signature="create_state_prep(num_qubits)",
        description="Return a QuantumCircuit that prepares the state |1> on an n-qubit register.",
        return_format="Return only the resulting QuantumCircuit.",
    ),
    11: TaskSpec(
        task_id=11,
        class_id=CLASS_ID,
        difficulty="basic",
        entrypoint="get_statevector",
        signature="get_statevector(circuit)",
        description="Compute and return the statevector corresponding to the input circuit.",
        return_format="Return only the resulting Statevector object.",
    ),
    39: TaskSpec(
        task_id=39,
        class_id=CLASS_ID,
        difficulty="basic",
        entrypoint="create_uniform_superposition",
        signature="create_uniform_superposition(n)",
        description="Initialize a uniform superposition on n qubits and return its statevector.",
        return_format="Return only the resulting Statevector object.",
    ),
    62: TaskSpec(
        task_id=62,
        class_id=CLASS_ID,
        difficulty="intermediate",
        entrypoint="bb84_senders_circuit",
        signature="bb84_senders_circuit(state, basis)",
        description="Construct a BB84 protocol circuit for the sender, inputting both the states and the measured bases.",
        return_format="Return only the resulting QuantumCircuit.",
    ),
    66: TaskSpec(
        task_id=66,
        class_id=CLASS_ID,
        difficulty="intermediate",
        entrypoint="w_state",
        signature="w_state()",
        description="Generate a QuantumCircuit for a 3-qubit W state and measure it.",
        return_format="Return only the measured QuantumCircuit.",
    ),
    139: TaskSpec(
        task_id=139,
        class_id=CLASS_ID,
        difficulty="intermediate",
        entrypoint="schmidt_test",
        signature="schmidt_test(data, qargs_B)",
        description="Return the Schmidt decomposition coefficients and subsystem vectors for the given density matrix and partition.",
        return_format=(
            "Return a sequence of Schmidt decomposition terms. Each term must contain exactly "
            "three elements: coefficient, subsystem state for A, and subsystem state for B."
        ),
    ),
}


def get_task_spec(task_id: int) -> TaskSpec:
    try:
        return TASK_SPECS[task_id]
    except KeyError as exc:
        raise ValueError(f"Unsupported task id: {task_id}") from exc


def bell_circuit() -> Any:
    from qiskit import QuantumCircuit

    circuit = QuantumCircuit(2)
    circuit.h(0)
    circuit.cx(0, 1)
    return circuit


def schmidt_state() -> Any:
    from qiskit.quantum_info import random_statevector

    return random_statevector(4, seed=42)


def build_cases() -> dict[int, list[dict[str, Any]]]:
    return {
        2: [{"label": "default", "args": ()}],
        3: [{"label": "drawing_false", "args": (False,)}],
        5: [{"label": "default", "args": ()}],
        6: [{"label": "num_qubits_3", "args": (3,)}],
        11: [{"label": "bell_state", "args": (bell_circuit(),)}],
        39: [{"label": "n3", "args": (3,)}],
        62: [
            {"label": "z_one", "args": ([1], [0])},
            {"label": "x_zero", "args": ([0], [1])},
            {"label": "mixed_four_qubits", "args": ([0, 1, 1, 0], [0, 0, 1, 1])},
        ],
        66: [{"label": "default", "args": ()}],
        139: [{"label": "random_state_seed_42_qargs_1", "args": (schmidt_state(), [1])}],
    }
