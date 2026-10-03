# EVAL_META: task_id=78, framework=cirq, class=3
import cirq

def qft_no_swaps(num_qubits):
    qubits = cirq.LineQubit.range(num_qubits)
    circuit = cirq.Circuit()
    
    for i in range(num_qubits - 1, -1, -1):
        for j in range(num_qubits - 1, i, -1):
            k = j - i + 1
            exponent = -1.0 / (2 ** (k - 1))
            circuit.append(cirq.CZ(qubits[j], qubits[i]) ** exponent)
        circuit.append(cirq.H(qubits[i]))
        
    return circuit
