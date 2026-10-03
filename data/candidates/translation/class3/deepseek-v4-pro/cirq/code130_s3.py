# EVAL_META: task_id=130, framework=cirq, class=3
import cirq

def inv_circuit(n):
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit()
    
    # Apply Hadamard to the second and third qubits (0-indexed: 1 and 2)
    circuit.append([cirq.H(qubits[1]), cirq.H(qubits[2])])
    
    # Apply CNOT between second and fourth, third and fifth
    circuit.append([cirq.CNOT(qubits[1], qubits[3]), cirq.CNOT(qubits[2], qubits[4])])
    
    return circuit**-1
