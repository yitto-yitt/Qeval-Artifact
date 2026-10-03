# EVAL_META: task_id=109, framework=qpanda2, class=3
from pyqpanda import *
from pyqpanda import var

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)

def circuit():
    vqc = VariationalQuantumCircuit()
    vqc.insert(H(qubits[0]))
    theta = var(0.0)
    vqc.insert(RZ(qubits[0], theta))
    return vqc

machine.finalize()
