# EVAL_META: task_id=109, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(1)

def circuit():
    theta = var(0.0, True, 'th')
    qc = VariationalQuantumCircuit(q)
    qc.insert(H(q[0]))
    qc.insert(RZ(q[0], theta))
    return qc

machine.finalize()
