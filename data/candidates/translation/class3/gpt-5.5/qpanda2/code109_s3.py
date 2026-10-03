# EVAL_META: task_id=109, framework=qpanda2, class=3
from pyqpanda import *
import atexit

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(1)
atexit.register(machine.finalize)

def circuit():
    theta = var(0.0, True)
    qc = VariationalQuantumCircuit()
    qc.insert(VariationalQuantumGate_H(q[0]))
    qc.insert(VariationalQuantumGate_RZ(q[0], theta))
    return qc
