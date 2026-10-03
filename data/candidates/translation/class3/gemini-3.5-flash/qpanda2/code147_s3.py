# EVAL_META: task_id=147, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(5)

def mcy(qc):
    ctrl_qubits = QVec()
    for i in range(4):
        ctrl_qubits.append(qubits[i])
    qc << Y(qubits[4]).control(ctrl_qubits)
    return qc

machine.finalize()
