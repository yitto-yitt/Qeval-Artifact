# EVAL_META: task_id=69, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, S, Sdg

def create_quantum_circuit_based_h0_cs01_h1_csdg10():
    qc = QCircuit()
    qc << H(0)
    qc << S(1).control(0)
    qc << H(1)
    qc << Sdg(0).control(1)
    return qc
