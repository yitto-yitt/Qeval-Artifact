# EVAL_META: task_id=69, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, S, Sdg, C

def create_quantum_circuit_based_h0_cs01_h1_csdg10():
    qc = QCircuit()
    qc << H(0)
    qc << C(S, 0, 1)
    qc << H(1)
    qc << C(Sdg, 1, 0)
    return qc
