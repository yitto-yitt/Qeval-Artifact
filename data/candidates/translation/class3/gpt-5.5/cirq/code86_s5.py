# EVAL_META: task_id=86, framework=cirq, class=3
import cirq


def collect_linear_blocks_with_and_without_limit():
    qubits = cirq.LineQubit.range(5)

    full_linear_circuit = cirq.Circuit(
        cirq.CNOT(qubits[0], qubits[1]),
        cirq.CNOT(qubits[1], qubits[2]),
        cirq.CNOT(qubits[2], qubits[3]),
        cirq.CNOT(qubits[3], qubits[4]),
    )
    full_linear_gate = cirq.MatrixGate(
        full_linear_circuit.unitary(qubit_order=qubits),
        name="LinearFunction",
    )

    first_limited_circuit = cirq.Circuit(
        cirq.CNOT(qubits[0], qubits[1]),
        cirq.CNOT(qubits[1], qubits[2]),
    )
    first_limited_gate = cirq.MatrixGate(
        first_limited_circuit.unitary(qubit_order=qubits[:3]),
        name="LinearFunction",
    )

    second_limited_circuit = cirq.Circuit(
        cirq.CNOT(qubits[2], qubits[3]),
        cirq.CNOT(qubits[3], qubits[4]),
    )
    second_limited_gate = cirq.MatrixGate(
        second_limited_circuit.unitary(qubit_order=qubits[2:5]),
        name="LinearFunction",
    )

    full_block = cirq.Circuit(
        cirq.H(qubits[0]),
        full_linear_gate.on(*qubits),
    )

    limited_block = cirq.Circuit(
        cirq.H(qubits[0]),
        first_limited_gate.on(*qubits[:3]),
        second_limited_gate.on(*qubits[2:5]),
    )

    return full_block, limited_block
