# EVAL_META: task_id=58, framework=qpanda, class=3
from pyqpanda3.core import *
from numpy import pi

def create_ch_gate():
    qvm = CPUQVM()
    qvm.init()
    q = qvm.qAlloc_many(2)
    circuit = QCircuit()
    circuit << RY(q[1], pi / 4)
    circuit << CNOT(q[0], q[1])
    circuit << RY(q[1], -pi / 4)
    return circuit
