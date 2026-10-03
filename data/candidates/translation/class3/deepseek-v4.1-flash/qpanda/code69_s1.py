# EVAL_META: task_id=69, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, CU1
from math import pi

def create_quantum_circuit_based_h0_cs01_h1_csdg10():
    qc = QCircuit()
    qc << H(0)
    qc << CU1(0, 1, pi/2)
    qc << H(1)
    qc << CU1(1, 0, -pi/2)
    return qc
