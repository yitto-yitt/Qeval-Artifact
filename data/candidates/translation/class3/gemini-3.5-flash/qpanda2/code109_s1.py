# EVAL_META: task_id=109, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(1)

def circuit():
    vqc = VariationalQuantumCircuit()
    vqc.insert(VariationalQuantumGate_H(q[0]))
    theta = Var(0.0)
    vqc.insert(VariationalQuantumGate_RZ(q[0], theta))
    return vqc

machine.finalize()
