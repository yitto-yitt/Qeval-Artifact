# EVAL_META: task_id=67, framework=qiskit, class=1
import numpy as np
from qiskit import QuantumCircuit

def chsh_circuit(alice: int, bob: int) -> QuantumCircuit:
    """
    Design a CHSH circuit that takes Alice and Bob input bits and returns the measured QuantumCircuit.
    """
    qc = QuantumCircuit(2, 2)
    
    # Create EPR pair (Bell state)
    qc.h(0)
    qc.cx(0, 1)
    
    # Alice's measurement basis selection
    if alice == 1:
        qc.h(0)
        
    # Bob's measurement basis selection
    if bob == 0:
        qc.ry(-np.pi / 4, 1)
    elif bob == 1:
        qc.ry(np.pi / 4, 1)
        
    # Measure both qubits
    qc.measure([0, 1], [0, 1])
    
    return qc
