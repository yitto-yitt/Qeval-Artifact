# EVAL_META: task_id=109, framework=qpanda2, class=3
from pyqpanda import *
import numpy as np
import atexit

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(1)
th = var(np.array([[0.0]], dtype=float), True)
atexit.register(machine.finalize)

def circuit():
    qc = VariationalQuantumCircuit()
    qc.insert(VariationalQuantumGate_H(q[0]))
    qc.insert(VariationalQuantumGate_RZ(q[0], th))
    return qc
