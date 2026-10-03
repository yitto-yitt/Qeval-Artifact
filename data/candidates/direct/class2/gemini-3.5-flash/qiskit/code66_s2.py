# EVAL_META: task_id=66, framework=qiskit, class=2

import numpy as np
from qiskit import QuantumCircuit

def w_state():
    """
    Generates a QuantumCircuit for a 3-qubit W state and measures it.
    The W state is |W> = 1/sqrt(3) * (|001> + |010> + |100>).
    """
    qc = QuantumCircuit(3, 3)
    
    # Start by putting qubit 2 in state |1>
    qc.x(2)
    
    # Share excitation with qubit 1
    theta1 = 2 * np.arccos(1 / np.sqrt(3))
    qc.cry(theta1, 2, 1)
    qc.cx(1, 2)
    
    # Share excitation with qubit 0
    theta2 = np.pi / 2
    qc.cry(theta2, 1, 0)
    qc.cx(0, 1)
    
    # Measure all qubits
    qc.measure([0, 1, 2], [0, 1, 2])
    
    return qc
