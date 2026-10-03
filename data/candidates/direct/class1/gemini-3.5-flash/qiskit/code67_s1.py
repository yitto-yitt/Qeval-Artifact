# EVAL_META: task_id=67, framework=qiskit, class=1
import numpy as np
from qiskit import QuantumCircuit

def chsh_circuit(alice: int, bob: int) -> QuantumCircuit:
    qc = QuantumCircuit(2)
    # Create Bell state
    qc.h(0)
    qc.cnot(0, 1)
    
    # Alice's measurement basis
    if alice == 1:
        qc.ry(-np.pi / 2, 0)
        
    # Bob's measurement basis
    if bob == 0:
        qc.ry(-np.pi / 4, 1)
    elif bob == 1:
        qc.ry(np.pi / 4, 1)
        
    qc.measure_all()
    return qc
