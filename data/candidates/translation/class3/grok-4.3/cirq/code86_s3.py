# EVAL_META: task_id=86, framework=cirq, class=3
import cirq

def collect_linear_blocks_with_and_without_limit():
    qubits = cirq.LineQubit.range(5)
    full_op = cirq.CircuitOperation(cirq.FrozenCircuit(
        cirq.H(qubits[0]),
        cirq.CNOT(qubits[0], qubits[1]),
        cirq.CNOT(qubits[1], qubits[2]),
        cirq.CNOT(qubits[2], qubits[3]),
        cirq.CNOT(qubits[3], qubits[4])
    ))
    full_block = cirq.Circuit(full_op)
    block1 = cirq.CircuitOperation(cirq.FrozenCircuit(
        cirq.H(qubits[0]),
        cirq.CNOT(qubits[0], qubits[1]),
        cirq.CNOT(qubits[1], qubits[2])
    ))
    block2 = cirq.CircuitOperation(cirq.FrozenCircuit(
        cirq.CNOT(qubits[2], qubits[3]),
        cirq.CNOT(qubits[3], qubits[4])
    ))
    limited_block = cirq.Circuit(block1, block2)
    return full_block, limited_block
