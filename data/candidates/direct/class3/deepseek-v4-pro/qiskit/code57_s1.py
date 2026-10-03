# EVAL_META: task_id=57, framework=qiskit, class=3
from qiskit import QuantumCircuit

def create_swap_gate():
    """Create a SWAP gate using only CX gates.
    
    Returns:
        QuantumCircuit: A 2-qubit circuit implementing a SWAP using three CX gates.
    """
    qc = QuantumCircuit(2, name="swap")
    qc.cx(0, 1)
    qc.cx(1, 0)
    qc.cx(0, 1)
    return qc
