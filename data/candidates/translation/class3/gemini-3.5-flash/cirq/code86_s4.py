# EVAL_META: task_id=86, framework=cirq, class=3
import cirq

def collect_linear_blocks_with_and_without_limit():
    qubits = cirq.LineQubit.range(5)
    
    # Full block circuit
    full_circuit = cirq.Circuit()
    full_circuit.append(cirq.H(qubits[0]))
    
    # Linear block for full
    block_full = cirq.Circuit(
        cirq.CNOT(qubits[0], qubits[1]),
        cirq.CNOT(qubits[1], qubits[2]),
        cirq.CNOT(qubits[2], qubits[3]),
        cirq.CNOT(qubits[3], qubits[4])
    )
    full_circuit.append(cirq.CircuitOperation(block_full.freeze()))
    
    # Limited block circuit
    limited_circuit = cirq.Circuit()
    limited_circuit.append(cirq.H(qubits[0]))
    
    # First block (qubits 0, 1, 2)
    block1 = cirq.Circuit(
        cirq.CNOT(qubits[0], qubits[1]),
        cirq.CNOT(qubits[1], qubits[2])
    )
    # Second block (qubits 2, 3, 4)
    block2 = cirq.Circuit(
        cirq.CNOT(qubits[2], qubits[3]),
        cirq.CNOT(qubits[3], qubits[4])
    )
    
    limited_circuit.append(cirq.CircuitOperation(block1.freeze()))
    limited_circuit.append(cirq.CircuitOperation(block2.freeze()))
    
    return full_circuit, limited_circuit
