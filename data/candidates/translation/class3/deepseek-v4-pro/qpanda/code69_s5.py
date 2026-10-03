# EVAL_META: task_id=69, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit
from math import pi

def create_quantum_circuit_based_h0_cs01_h1_csdg10():
    qc = QuantumCircuit()
    q = qc.qAlloc_many(2)
    qc.h(q[0])
    qc.cphase(q[0], q[1], pi / 2)
    qc.h(q[1])
    qc.cphase(q[1], q[0], -pi / 2)
    return qc
