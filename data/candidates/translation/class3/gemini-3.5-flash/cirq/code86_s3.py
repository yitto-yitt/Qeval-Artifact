# EVAL_META: task_id=86, framework=cirq, class=3
import cirq

def collect_linear_blocks_with_and_without_limit():
    qubits = cirq.LineQubit.range(5)
    
    # Full block circuit
    sub_full = cirq.Circuit(
        cirq.CNOT(qubits[0], qubits[1]),
        cirq.CNOT(qubits[1], qubits[2]),
        cirq.CNOT(qubits[2], qubits[3]),
        cirq.CNOT(qubits[3], qubits[4])
    )
    full_block = cirq.Circuit(
        cirq.H(qubits[0]),
        cirq.CircuitOperation(sub_full.freeze())
    )
    
    # Limited block circuit
    sub_lim1 = cirq.Circuit(
        cirq.CNOT(qubits[0], qubits[1]),
        cirq.CNOT(qubits[1], qubits[2])
    )
    sub_lim2 = cirq.Circuit(
        cirq.CNOT(qubits[2], qubits[3]),
        cirq.CNOT(qubits[3], qubits[4])
    )
    limited_block = cirq.Circuit(
        cirq.H(qubits[0]),
        cirq.CircuitOperation(sub_lim1.freeze()),
        cirq.CircuitOperation(sub_lim2.freeze())
    )
    
    return full_block, limited_block
