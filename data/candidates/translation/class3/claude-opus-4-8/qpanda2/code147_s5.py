# EVAL_META: task_id=147, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(5)

def mcy(qc):
    controls = qubits[0:4]
    target = qubits[4]
    qc << Y(target).control(controls)
    return qc

machine.finalize()
