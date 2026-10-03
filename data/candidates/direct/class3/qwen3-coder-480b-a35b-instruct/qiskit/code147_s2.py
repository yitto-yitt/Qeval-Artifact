# EVAL_META: task_id=147, framework=qiskit, class=3
from qiskit import QuantumCircuit


def mcy(qc):
    """
    Adds a multi-controlled-Y operation to qubit 4, controlled by qubits 0-3.
    
    Args:
        qc (QuantumCircuit): The quantum circuit to apply the operation to.
        
    Returns:
        QuantumCircuit: The modified quantum circuit.
    """
    # Apply multi-controlled Y gate with qubits 0, 1, 2, 3 as controls and qubit 4 as target
    qc.mcry(3.141592653589793, [0, 1, 2, 3], 4)
    return qc
