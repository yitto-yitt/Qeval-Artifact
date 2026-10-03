# EVAL_META: task_id=62, framework=qiskit, class=2
from qiskit import QuantumCircuit

def bb84_senders_circuit(state, basis):
    """
    Constructs a BB84 protocol circuit for the sender.
    
    Parameters:
    - state: The bit to send (0 or 1, as int or str)
    - basis: The basis to encode in ('Z'/'rect' for computational, 'X'/'diag' for diagonal)
    
    Returns:
    - QuantumCircuit: The prepared quantum circuit.
    """
    qc = QuantumCircuit(1)
    
    # Prepare the state |1> if state is 1
    if str(state) == '1' or state == 1:
        qc.x(0)
        
    # Apply Hadamard if basis is diagonal (X basis)
    basis_str = str(basis).strip().upper()
    if basis_str in ['X', 'H', 'DIAG', 'D', '1']:
        qc.h(0)
        
    return qc
