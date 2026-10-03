# EVAL_META: task_id=62, framework=qiskit, class=2

from qiskit import QuantumCircuit

def bb84_senders_circuit(state, basis):
    """
    Constructs a BB84 protocol circuit for the sender.
    
    Args:
        state (list): A list of bits (0 or 1) representing the state to encode.
        basis (list): A list of bases (0/'Z' for rectilinear, 1/'X' for diagonal).
        
    Returns:
        QuantumCircuit: The constructed QuantumCircuit.
    """
    n = len(state)
    qc = QuantumCircuit(n)
    for i in range(n):
        # Apply X gate if the state bit is 1
        if state[i] in [1, '1', True]:
            qc.x(i)
        # Apply H gate if the basis is X (diagonal)
        if basis[i] in [1, '1', 'X', 'x', True]:
            qc.h(i)
    return qc
