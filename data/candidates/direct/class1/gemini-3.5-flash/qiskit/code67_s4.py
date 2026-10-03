# EVAL_META: task_id=67, framework=qiskit, class=1
import numpy as np
from qiskit import QuantumCircuit

def chsh_circuit(alice: int, bob: int) -> QuantumCircuit:
    """
    Design a CHSH circuit that takes Alice and Bob input bits and returns the measured QuantumCircuit.
    
    Alice's inputs:
    - 0: Measure in Z basis (no rotation)
    - 1: Measure in X basis (rotate by -pi/2 around Y)
    
    Bob's inputs:
    - 0: Measure in basis rotated by pi/8 (rotate by -pi/4 around Y)
    - 1: Measure in basis rotated by -pi/8 (rotate by pi/4 around Y)
    """
    qc = QuantumCircuit(2, 2)
    
    # Create the Bell state |Phi+> = (|00> + |11>) / sqrt(2)
    qc.h(0)
    qc.cx(0, 1)
    
    # Alice's measurement selection
    if alice == 1:
        qc.ry(-np.pi / 2, 0)
        
    # Bob's measurement selection
    if bob == 0:
        qc.ry(-np.pi / 4, 1)
    elif bob == 1:
        qc.ry(np.pi / 4, 1)
        
    # Measure the qubits
    qc.measure([0, 1], [0, 1])
    
    return qc
