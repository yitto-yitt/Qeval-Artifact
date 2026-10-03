# EVAL_META: task_id=130, framework=cirq, class=3
import cirq

def inv_circuit(n):
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit()
    
    # Apply Hadamard gates to the second and third qubits (indices 1 and 2)
    for i in range(2):
        circuit.append(cirq.H(qubits[i + 1]))
    
    # Apply CNOT gates between the second and fourth qubits, and between the third and fifth qubits
    for i in range(2):
        circuit.append(cirq.CNOT(qubits[i + 1], qubits[i + 2 + 1]))
    
    # Return the inverse of the circuit
    return circuit**-1
