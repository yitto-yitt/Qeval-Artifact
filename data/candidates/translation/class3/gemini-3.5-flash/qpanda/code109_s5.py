# EVAL_META: task_id=109, framework=qpanda, class=3
from pyqpanda3.core import *

def circuit():
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(1)
    vqc = VariationalQuantumCircuit()
    theta = var(0.0, True)
    vqc << VariationalQuantumGate_H(q[0]) << VariationalQuantumGate_RZ(q[0], theta)
    return vqc
