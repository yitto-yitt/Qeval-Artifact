# EVAL_META: task_id=86, framework=cirq, class=3
import cirq

def collect_linear_blocks_with_and_without_limit():
    qubits = cirq.LineQubit.range(5)
    
    # Full block: H on qubit 0, then linear block on all 5 qubits
    full_sub = cirq.Circuit(
        cirq.CX(qubits[0], qubits[1]),
        cirq.CX(qubits[1], qubits[2]),
        cirq.CX(qubits[2], qubits[3]),
        cirq.CX(qubits[3], qubits[4])
    )
    full_unitary = cirq.unitary(full_sub)
    full_circuit = cirq.Circuit(
        cirq.H(qubits[0]),
        cirq.MatrixGate(full_unitary).on(*qubits)
    )
    
    # Limited block: max_block_width=3
    block1_sub = cirq.Circuit(
        cirq.CX(qubits[0], qubits[1]),
        cirq.CX(qubits[1], qubits[2])
    )
    block1_unitary = cirq.unitary(block1_sub)
    
    block2_sub = cirq.Circuit(
        cirq.CX(qubits[2], qubits[3]),
        cirq.CX(qubits[3], qubits[4])
    )
    block2_unitary = cirq.unitary(block2_sub)
    
    limited_circuit = cirq.Circuit(
        cirq.H(qubits[0]),
        cirq.MatrixGate(block1_unitary).on(qubits[0], qubits[1], qubits[2]),
        cirq.MatrixGate(block2_unitary).on(qubits[2], qubits[3], qubits[4])
    )
    
    return full_circuit, limited_circuit
