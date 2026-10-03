# EVAL_META: task_id=70, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, CSWAP, Sdg

def create_quantum_circuit_based_h0_cswap012_h1_csdg10():
    qc = QCircuit()
    qc << H(0)
    qc << CSWAP(0, 1, 2)
    qc << H(1)
    qc << Sdg(0).control(1)
    return qc
