# EVAL_META: task_id=67, framework=qiskit, class=1
from qiskit import QuantumCircuit
import numpy as np

def chsh_circuit(alice, bob):
    qc = QuantumCircuit(2, 2)
    # Create Bell state
    qc.h(0)
    qc.cx(0, 1)
    
    # Alice's measurement setting
    if alice == 1:
        qc.ry(np.pi / 2, 0)
        
    # Bob's measurement setting
    if bob == 0:
        qc.ry(np.pi / 4, 1)
    else:
        qc.ry(-np.pi / 4, 1)
        
    qc.measure([0, 1], [0, 1])
    return qc
