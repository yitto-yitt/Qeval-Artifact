# EVAL_META: task_id=147, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = qAlloc_many(5)

def mcy(qc):
    gate = Y(qubits[4]).control([qubits[0], qubits[1], qubits[2], qubits[3]])
    qc << gate
    return qc

machine.finalize()
