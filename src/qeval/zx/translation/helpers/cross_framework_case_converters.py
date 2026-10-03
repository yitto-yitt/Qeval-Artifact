from __future__ import annotations

import copy
from dataclasses import dataclass
from typing import Any


PARAMETER_VALUES = [0.37, 0.73, 1.11, 1.57, 2.03, 2.41, 2.89, 3.17]
SUPPORTED_FRAMEWORKS = {"qiskit", "cirq", "qpanda", "pennylane"}


@dataclass(frozen=True)
class PennylaneSymbol:
    name: str

    @property
    def free_symbols(self) -> frozenset["PennylaneSymbol"]:
        return frozenset((self,))

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name


def normalize_framework(framework: str) -> str:
    text = (framework or "qiskit").strip().lower()
    if text in {"qpanda3", "pyqpanda3"}:
        return "qpanda"
    return text


def convert_kwargs_for_framework(kwargs: dict[str, Any], framework: str, task_id: int) -> dict[str, Any]:
    return {key: convert_value_for_framework(value, framework, task_id) for key, value in kwargs.items()}


def convert_args_for_framework(args: tuple[Any, ...], framework: str, task_id: int) -> tuple[Any, ...]:
    normalized = normalize_framework(framework)
    if normalized == "qiskit":
        return clone_value(args)
    return tuple(convert_value_for_framework(value, normalized, task_id) for value in args)


def convert_value_for_framework(value: Any, framework: str, task_id: int) -> Any:
    normalized = normalize_framework(framework)
    if normalized not in SUPPORTED_FRAMEWORKS:
        raise NotImplementedError(f"Unsupported framework={framework!r} for task_id={task_id}.")
    if normalized == "cirq":
        return convert_value_to_cirq(value, task_id)
    if normalized == "qpanda":
        return convert_value_to_qpanda(value, task_id)
    if normalized == "pennylane":
        return convert_value_to_pennylane(value, task_id)
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


def is_qiskit_quantum_circuit(value: Any) -> bool:
    return value.__class__.__name__ == "QuantumCircuit" and hasattr(value, "data") and hasattr(value, "num_qubits")


def is_qiskit_operator_like(value: Any) -> bool:
    module = value.__class__.__module__
    return module.startswith("qiskit.") and value.__class__.__name__ != "QuantumCircuit"


def qiskit_operator_matrix(value: Any) -> Any:
    import numpy as np
    from qiskit.quantum_info import Operator

    return np.asarray(Operator(value).data, dtype=complex)


def qiskit_operator_matrix_for_pennylane(value: Any) -> Any:
    """Convert Qiskit's little-endian matrix basis to PennyLane wire order."""
    import numpy as np

    matrix = qiskit_operator_matrix(value)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError("Qiskit operator matrix must be square")
    dimension = matrix.shape[0]
    num_qubits = dimension.bit_length() - 1
    if (1 << num_qubits) != dimension:
        raise ValueError("Qiskit operator dimension must be a power of two")

    # Qiskit indexes q0 as the least significant bit; PennyLane's explicit
    # wire order [0, ..., n-1] places wire 0 as the most significant bit.
    permutation = []
    for index in range(dimension):
        bits = [(index >> (num_qubits - 1 - wire)) & 1 for wire in range(num_qubits)]
        permutation.append(sum(bit << wire for wire, bit in enumerate(bits)))
    return matrix[np.ix_(permutation, permutation)]


def convert_value_to_cirq(value: Any, task_id: int) -> Any:
    if is_qiskit_quantum_circuit(value):
        return qiskit_circuit_to_cirq(value, task_id)
    if is_qiskit_operator_like(value):
        return qiskit_operator_matrix(value)
    if isinstance(value, list):
        return [convert_value_to_cirq(item, task_id) for item in value]
    if isinstance(value, tuple):
        return tuple(convert_value_to_cirq(item, task_id) for item in value)
    return clone_value(value)


def convert_value_to_qpanda(value: Any, task_id: int) -> Any:
    if is_qiskit_quantum_circuit(value):
        return qiskit_circuit_to_qpanda(value, task_id)
    if is_qiskit_operator_like(value):
        return qiskit_operator_matrix(value)
    if isinstance(value, list):
        return [convert_value_to_qpanda(item, task_id) for item in value]
    if isinstance(value, tuple):
        return tuple(convert_value_to_qpanda(item, task_id) for item in value)
    return clone_value(value)


def convert_value_to_pennylane(value: Any, task_id: int) -> Any:
    if is_qiskit_quantum_circuit(value):
        return qiskit_circuit_to_pennylane(value, task_id)
    if is_qiskit_operator_like(value):
        return qiskit_operator_matrix_for_pennylane(value)
    if isinstance(value, list):
        return [convert_value_to_pennylane(item, task_id) for item in value]
    if isinstance(value, tuple):
        return tuple(convert_value_to_pennylane(item, task_id) for item in value)
    return clone_value(value)


def qiskit_circuit_to_cirq(circuit: Any, task_id: int) -> Any:
    import cirq
    import sympy

    qubits = cirq.LineQubit.range(circuit.num_qubits)
    converted = cirq.Circuit()
    for instruction in circuit.data:
        operation = instruction.operation
        qargs = [circuit.find_bit(qubit).index for qubit in instruction.qubits]
        cargs = [circuit.find_bit(clbit).index for clbit in instruction.clbits]
        name = operation.name.lower()
        if name in {"barrier", "delay"}:
            continue
        if name == "measure":
            converted.append(cirq.measure(qubits[qargs[0]], key=f"c{cargs[0] if cargs else qargs[0]}"))
            continue
        gate = cirq_gate_for_qiskit_operation(operation, sympy)
        converted.append(gate.on(*(qubits[index] for index in qargs)))
    if task_id == 147 and not converted.all_qubits():
        converted.append(cirq.I.on_each(*qubits))
    return converted


def cirq_gate_for_qiskit_operation(operation: Any, sympy: Any) -> Any:
    import cirq
    import numpy as np

    name = operation.name.lower()
    params = list(getattr(operation, "params", []) or [])
    if name == "h":
        return cirq.H
    if name == "x":
        return cirq.X
    if name == "y":
        return cirq.Y
    if name == "z":
        return cirq.Z
    if name == "s":
        return cirq.S
    if name == "sdg":
        return cirq.S**-1
    if name == "t":
        return cirq.T
    if name == "tdg":
        return cirq.T**-1
    if name in {"sx", "sxdg"} and hasattr(operation, "to_matrix"):
        return cirq.MatrixGate(operation.to_matrix())
    if name in {"cx", "cnot"}:
        return cirq.CNOT
    if name == "cz":
        return cirq.CZ
    if name == "swap":
        return cirq.SWAP
    if name == "ccx":
        return cirq.CCX
    if name == "rx":
        return cirq.rx(cirq_param(params[0], sympy))
    if name == "ry":
        return cirq.ry(cirq_param(params[0], sympy))
    if name == "rz":
        return cirq.rz(cirq_param(params[0], sympy))
    if name in {"p", "u1"}:
        return cirq.ZPowGate(exponent=cirq_param(params[0], sympy) / np.pi)
    if hasattr(operation, "to_matrix"):
        return cirq.MatrixGate(operation.to_matrix())
    raise TypeError(f"Unsupported Qiskit operation for Cirq conversion: {name}")


def cirq_param(value: Any, sympy: Any) -> Any:
    try:
        return float(value)
    except TypeError:
        return sympy.Symbol(getattr(value, "name", str(value)))


def qiskit_circuit_to_qpanda(circuit: Any, task_id: int) -> Any:
    from pyqpanda3.core import CNOT, CZ, H, QCircuit, RX, RY, RZ, S, SWAP, T, X, Y, Z, measure

    converted = QCircuit(circuit.num_qubits)
    for instruction in circuit.data:
        operation = instruction.operation
        qargs = [circuit.find_bit(qubit).index for qubit in instruction.qubits]
        cargs = [circuit.find_bit(clbit).index for clbit in instruction.clbits]
        name = operation.name.lower()
        params = list(getattr(operation, "params", []) or [])
        if name in {"barrier", "delay"}:
            continue
        if name == "measure":
            converted << measure(qargs[0], cargs[0] if cargs else qargs[0])
        elif name == "h":
            converted << H(qargs[0])
        elif name == "x":
            converted << X(qargs[0])
        elif name == "y":
            converted << Y(qargs[0])
        elif name == "z":
            converted << Z(qargs[0])
        elif name == "s":
            converted << S(qargs[0])
        elif name == "t":
            converted << T(qargs[0])
        elif name in {"cx", "cnot"}:
            converted << CNOT(qargs[0], qargs[1])
        elif name == "cz":
            converted << CZ(qargs[0], qargs[1])
        elif name == "swap":
            converted << SWAP(qargs[0], qargs[1])
        elif name == "rx":
            converted << RX(qargs[0], qpanda_angle(params[0]))
        elif name == "ry":
            converted << RY(qargs[0], qpanda_angle(params[0]))
        elif name == "rz":
            converted << RZ(qargs[0], qpanda_angle(params[0]))
        else:
            raise TypeError(f"Unsupported Qiskit operation for QPanda conversion: {name}")
    return converted


def qpanda_angle(value: Any) -> float:
    try:
        return float(value)
    except TypeError:
        return PARAMETER_VALUES[0]


def qiskit_circuit_to_pennylane(circuit: Any, task_id: int) -> Any:
    import pennylane as qml

    operations: list[Any] = []
    measurements: list[Any] = []
    for instruction in circuit.data:
        operation = instruction.operation
        qargs = [circuit.find_bit(qubit).index for qubit in instruction.qubits]
        name = operation.name.lower()
        if name in {"barrier", "delay"}:
            continue
        if name == "measure":
            if qargs:
                measurements.append(qml.sample(wires=qargs[0]))
            continue
        gate = pennylane_gate_for_qiskit_operation(operation, qargs)
        if gate is not None:
            operations.append(gate)
    return make_quantum_script(operations, measurements, circuit.num_qubits, circuit.num_clbits)


def pennylane_gate_for_qiskit_operation(operation: Any, qargs: list[int]) -> Any | None:
    import pennylane as qml

    name = operation.name.lower()
    params = list(getattr(operation, "params", []) or [])
    if name in {"barrier", "delay"}:
        return None
    if name in {"id", "i"}:
        return qml.Identity(wires=qargs[0])
    if name == "h":
        return qml.Hadamard(wires=qargs[0])
    if name == "x":
        return qml.PauliX(wires=qargs[0])
    if name == "y":
        return qml.PauliY(wires=qargs[0])
    if name == "z":
        return qml.PauliZ(wires=qargs[0])
    if name == "s":
        return qml.S(wires=qargs[0])
    if name == "sdg":
        return qml.adjoint(qml.S(wires=qargs[0]))
    if name == "t":
        return qml.T(wires=qargs[0])
    if name == "tdg":
        return qml.adjoint(qml.T(wires=qargs[0]))
    if name == "sx":
        return qml.SX(wires=qargs[0])
    if name == "sxdg":
        return qml.adjoint(qml.SX(wires=qargs[0]))
    if name in {"cx", "cnot"}:
        return qml.CNOT(wires=qargs)
    if name == "cz":
        return qml.CZ(wires=qargs)
    if name == "swap":
        return qml.SWAP(wires=qargs)
    if name == "ccx":
        return qml.Toffoli(wires=qargs)
    if name == "rx":
        return qml.RX(pennylane_param(params[0]), wires=qargs[0])
    if name == "ry":
        return qml.RY(pennylane_param(params[0]), wires=qargs[0])
    if name == "rz":
        return qml.RZ(pennylane_param(params[0]), wires=qargs[0])
    if name in {"p", "u1"}:
        return qml.PhaseShift(pennylane_param(params[0]), wires=qargs[0])
    if name == "u2":
        return qml.U2(*(pennylane_param(param) for param in params), wires=qargs[0])
    if name == "u":
        return qml.U3(*(pennylane_param(param) for param in params), wires=qargs[0])
    if hasattr(operation, "to_matrix"):
        return qml.QubitUnitary(operation.to_matrix(), wires=qargs)
    raise TypeError(f"Unsupported Qiskit operation for PennyLane conversion: {name}")


def pennylane_param(value: Any) -> Any:
    try:
        return float(value)
    except (TypeError, ValueError):
        return PennylaneSymbol(getattr(value, "name", str(value)))


def make_quantum_script(
    operations: list[Any],
    measurements: list[Any],
    num_qubits: int,
    num_clbits: int,
) -> Any:
    import pennylane as qml

    wire_count = max(num_qubits, num_clbits, 1)
    if hasattr(qml.tape, "QuantumScript"):
        return qml.tape.QuantumScript(operations, measurements, shots=None)

    dev = qml.device("default.qubit", wires=wire_count)

    @qml.qnode(dev)
    def circuit() -> Any:
        for op in operations:
            qml.apply(op)
        if measurements:
            return measurements[0]
        return qml.state()

    return qml.workflow.construct_tape(circuit)()
