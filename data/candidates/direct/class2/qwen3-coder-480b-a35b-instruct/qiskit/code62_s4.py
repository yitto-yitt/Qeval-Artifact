# EVAL_META: task_id=62, framework=qiskit, class=2
from qiskit import QuantumCircuit


def bb84_senders_circuit(state, basis):
    """
    Constructs a BB84 protocol circuit for the sender.
    
    Args:
        state (list): List of bits representing the quantum states to prepare.
        basis (list): List of bits representing the measurement bases.
        
    Returns:
        QuantumCircuit: The constructed quantum circuit.
    """
    n = len(state)
    qc = QuantumCircuit(n, n)
    
    for i in range(n):
        if state[i] == 1:
            qc.x(i)  # Prepare |1> state
        
        if basis[i] == 1:
            qc.h(i)  # Change to X basis (Hadamard gate)
    
    # Measure all qubits
    for i in range(n):
        qc.measure(i, i)
    
    return qc
