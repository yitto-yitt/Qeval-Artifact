# EVAL_META: task_id=49, framework=qiskit, class=3

from qiskit import QuantumCircuit

def simple_elitzur_vaidman():
    # Qubit 0: Photon path (0 for path A, 1 for path B)
    # Qubit 1: Bomb state (0 for unfired, 1 for exploded)
    qc = QuantumCircuit(2)
    
    # First beamsplitter
    qc.h(0)
    
    # Interaction with the bomb (if photon is in path B, the bomb explodes)
    qc.cx(0, 1)
    
    # Second beamsplitter
    qc.h(0)
    
    return qc
