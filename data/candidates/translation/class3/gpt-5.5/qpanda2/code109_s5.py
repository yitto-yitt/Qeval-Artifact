# EVAL_META: task_id=109, framework=qpanda2, class=3
import atexit
from pyqpanda import CPUQVM, VariationalQuantumCircuit, VariationalQuantumGate_H, VariationalQuantumGate_RZ, var

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(1)
theta = var(0.0, True)

def circuit():
    qc = VariationalQuantumCircuit()
    qc.insert(VariationalQuantumGate_H(q[0]))
    qc.insert(VariationalQuantumGate_RZ(q[0], theta))
    return qc

atexit.register(machine.finalize)
