# EVAL_META: task_id=62, framework=qiskit, class=2
from qiskit import QuantumCircuit

def bb84_senders_circuit(state, basis):
    """Constructs a BB84 protocol circuit for the sender.
    
    Args:
        state (list or str): The secret bits to send (0 or 1).
        basis (list or str): The bases to encode the bits in (0 for Z, 1 for X).
        
    Returns:
        QuantumCircuit: The prepared sender's quantum circuit.
    """
    n = len(state)
    qc = QuantumCircuit(n)
    for i in range(n):
        if int(state[i]) == 1:
            qc.x(i)
        if int(basis[i]) == 1:
            qc.h(i)
    return qc
