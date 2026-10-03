# EVAL_META: task_id=38, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, CRZ, CRY, Qubit

def create_quantum_circuit_based_h0_crz01_h1_cry10(theta):
    qc = QCircuit()
    q0 = Qubit(0)
    q1 = Qubit(1)
    qc << H(q0)
    qc << CRZ(q0, q1, theta)
    qc << H(q1)
    qc << CRY(q1, q0, theta)
    return qc
