# EVAL_META: task_id=86, framework=cirq, class=3
import cirq

def collect_linear_blocks_with_and_without_limit():
    qubits = cirq.LineQubit.range(5)

    full_linear_block = cirq.FrozenCircuit(
        cirq.CNOT(qubits[0], qubits[1]),
        cirq.CNOT(qubits[1], qubits[2]),
        cirq.CNOT(qubits[2], qubits[3]),
        cirq.CNOT(qubits[3], qubits[4]),
    )
    full_block = cirq.Circuit(
        cirq.H(qubits[0]),
        cirq.CircuitOperation(full_linear_block),
    )

    limited_linear_block_1 = cirq.FrozenCircuit(
        cirq.CNOT(qubits[0], qubits[1]),
        cirq.CNOT(qubits[1], qubits[2]),
    )
    limited_linear_block_2 = cirq.FrozenCircuit(
        cirq.CNOT(qubits[2], qubits[3]),
        cirq.CNOT(qubits[3], qubits[4]),
    )
    limited_block = cirq.Circuit(
        cirq.H(qubits[0]),
        cirq.CircuitOperation(limited_linear_block_1),
        cirq.CircuitOperation(limited_linear_block_2),
    )

    return full_block, limited_block
