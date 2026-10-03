# EVAL_META: task_id=130, framework=cirq, class=3
import cirq

def inv_circuit(n):
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit()
    
    # Apply Hadamard gates to the second and third qubits (indices 1 and 2)
    circuit.append(cirq.H(qubits[1]))
    circuit.append(cirq.H(qubits[2]))
    
    # Apply CNOT gates between the second and fourth qubits, and between the third and fifth qubits
    circuit.append(cirq.CNOT(qubits[1], qubits[3]))
    circuit.append(cirq.CNOT(qubits[2], qubits[4]))
    
    # Return the inverse of the circuit
    return cirq.inverse(circuit)
