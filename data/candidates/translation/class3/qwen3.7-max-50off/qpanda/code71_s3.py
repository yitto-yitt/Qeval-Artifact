# EVAL_META: task_id=71, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, CSX, Qubit

def create_quantum_circuit_based_h0_csx01_h1():
    q0 = Qubit(0)
    q1 = Qubit(1)
    q2 = Qubit(2)
    
    qc = QCircuit()
    qc << H(q0)
    qc << CSX(q0, q1)
    qc << H(q1)
    
    return qc
