# EVAL_META: task_id=86, framework=cirq, class=3
import cirq

def collect_linear_blocks_with_and_without_limit():
    qubits = cirq.LineQubit.range(5)
    qc = cirq.Circuit(
        cirq.H(qubits[0]),
        cirq.CNOT(qubits[0], qubits[1]),
        cirq.CNOT(qubits[1], qubits[2]),
        cirq.CNOT(qubits[2], qubits[3]),
        cirq.CNOT(qubits[3], qubits[4])
    )
    full_block = cirq.Circuit(
        cirq.MatrixGate(cirq.unitary(qc)).on(*qubits)
    )
    qc1 = cirq.Circuit(
        cirq.H(qubits[0]),
        cirq.CNOT(qubits[0], qubits[1]),
        cirq.CNOT(qubits[1], qubits[2])
    )
    qc2 = cirq.Circuit(
        cirq.CNOT(qubits[2], qubits[3]),
        cirq.CNOT(qubits[3], qubits[4])
    )
    limited_block = cirq.Circuit(
        cirq.MatrixGate(cirq.unitary(qc1)).on(qubits[0], qubits[1], qubits[2]),
        cirq.MatrixGate(cirq.unitary(qc2)).on(qubits[2], qubits[3], qubits[4])
    )
    return full_block, limited_block
