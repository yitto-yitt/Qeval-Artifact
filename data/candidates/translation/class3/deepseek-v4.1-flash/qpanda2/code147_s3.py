# EVAL_META: task_id=147, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(5)

def mcy(qc):
    qc << Sdg(qubits[4]) << MCX(qubits[0:4], qubits[4]) << S(qubits[4])
    return qc

machine.finalize()
