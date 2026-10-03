# EVAL_META: task_id=23, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = qAlloc_many(3)

def dj_constant_oracle():
    circuit = QCircuit()
    circuit << X(q[2])
    return circuit

machine.finalize()
