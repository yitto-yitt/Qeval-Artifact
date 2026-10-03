# EVAL_META: task_id=57, framework=qiskit, class=3
from qiskit import QuantumCircuit

def create_swap_gate():
    """
    Creates a SWAP gate implemented using only CX (CNOT) gates.
    
    Returns:
        QuantumCircuit: A 2-qubit quantum circuit representing the SWAP gate.
    """
    qc = QuantumCircuit(2, name='swap_from_cx')
    qc.cx(0, 1)
    qc.cx(1, 0)
    qc.cx(0, 1)
    return qc
