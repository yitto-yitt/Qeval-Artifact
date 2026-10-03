# EVAL_META: task_id=109, framework=qpanda2, class=3
from pyqpanda import *
import numpy as np
import atexit

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)

atexit.register(machine.finalize)

def circuit():
    theta = var(np.array([0.0]), True)
    qc = VariationalQuantumCircuit()
    qc.insert(VariationalQuantumGate_H(qubits[0]))
    qc.insert(VariationalQuantumGate_RZ(qubits[0], theta))
    return qc
