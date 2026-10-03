# EVAL_META: task_id=38, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, RZ, RY

def create_quantum_circuit_based_h0_crz01_h1_cry10(theta):
    qc = QCircuit()
    qc.insert(H(0))
    qc.insert(RZ(1, theta).control(0))
    qc.insert(H(1))
    qc.insert(RY(0, theta).control(1))
    return qc
