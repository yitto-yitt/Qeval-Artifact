# EVAL_META: task_id=130, framework=qiskit, class=3
from qiskit import QuantumCircuit

def inv_circuit(n):
    qc = QuantumCircuit(n)
    
    # Apply Hadamard gates to second and third qubits (indices 1 and 2)
    qc.h(1)
    qc.h(2)
    
    # Apply CNOT gates between second and fourth qubits (1 and 3), and between third and fifth qubits (2 and 4)
    if n > 3:
        qc.cx(1, 3)
    if n > 4:
        qc.cx(2, 4)
    
    # Return the inverse of the circuit
    return qc.inverse()
