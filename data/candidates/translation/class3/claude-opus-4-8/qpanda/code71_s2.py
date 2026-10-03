# EVAL_META: task_id=71, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, S, X, T

def create_quantum_circuit_based_h0_csx01_h1():
    qc = QCircuit(3)
    qc << H(0)
    qc << H(1)
    qc << T(1)
    qc << X(1, 0)
    qc << T(1).dagger()
    qc << X(1, 0)
    qc << T(0)
    qc << H(1)
    qc << H(1)
    return qc
