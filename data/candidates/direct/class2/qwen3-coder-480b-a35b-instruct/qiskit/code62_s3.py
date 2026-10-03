# EVAL_META: task_id=62, framework=qiskit, class=2
from qiskit import QuantumCircuit


def bb84_senders_circuit(state, basis):
    """
    Constructs a BB84 protocol circuit for the sender.
    
    Args:
        state (list): List of bits representing the quantum states to prepare (0 or 1).
        basis (list): List of bits representing the basis to encode in (0 for Z-basis, 1 for X-basis).
        
    Returns:
        QuantumCircuit: The constructed quantum circuit.
    """
    n = len(state)
    qc = QuantumCircuit(n)
    
    for i in range(n):
        if state[i] == 1:
            qc.x(i)  # Prepare |1> state
        
        if basis[i] == 1:  # X-basis encoding
            qc.h(i)  # Apply Hadamard to switch to X-basis
    
    return qc
