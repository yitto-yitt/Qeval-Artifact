# EVAL_META: task_id=70, framework=qpanda, class=3
import math
from pyqpanda3.core import QuantumCircuit


def create_quantum_circuit_based_h0_cswap012_h1_csdg10():
    qc = QuantumCircuit(3)
    qc.h(0)
    qc.cswap(0, 1, 2)
    qc.h(1)
    qc.cphase(1, 0, -math.pi / 2)
    return qc
