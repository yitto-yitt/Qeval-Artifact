# EVAL_META: task_id=147, framework=qpanda, class=3
from pyqpanda3.core import Y, qAlloc_many

def mcy(qc):
    qubits = qAlloc_many(5)
    qc << Y(qubits[4]).control(qubits[0:4])
    return qc
