# EVAL_META: task_id=38, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, CRZ, CRY

def create_quantum_circuit_based_h0_crz01_h1_cry10(theta):
    qc = QCircuit(2)
    qc << H(0)
    qc << CRZ(0, 1, theta)
    qc << H(1)
    qc << CRY(1, 0, theta)
    return qc
