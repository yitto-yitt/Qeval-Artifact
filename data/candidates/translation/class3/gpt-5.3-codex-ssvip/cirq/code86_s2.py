# EVAL_META: task_id=86, framework=cirq, class=3
import cirq


def collect_linear_blocks_with_and_without_limit():
    qubits = cirq.LineQubit.range(5)
    ops = [
        cirq.H(qubits[0]),
        cirq.CNOT(qubits[0], qubits[1]),
        cirq.CNOT(qubits[1], qubits[2]),
        cirq.CNOT(qubits[2], qubits[3]),
        cirq.CNOT(qubits[3], qubits[4]),
    ]
    base_circuit = cirq.Circuit(ops)

    full_block = cirq.Circuit(cirq.CircuitOperation(base_circuit.freeze()))
    limited_block = cirq.Circuit(
        cirq.H(qubits[0]),
        cirq.CircuitOperation(cirq.Circuit([cirq.CNOT(qubits[0], qubits[1]), cirq.CNOT(qubits[1], qubits[2])]).freeze()),
        cirq.CircuitOperation(cirq.Circuit([cirq.CNOT(qubits[2], qubits[3]), cirq.CNOT(qubits[3], qubits[4])]).freeze()),
    )

    return full_block, limited_block
