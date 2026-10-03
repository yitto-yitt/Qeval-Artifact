# EVAL_META: task_id=147, framework=qpanda, class=3
from pyqpanda3.core import Y

def mcy(qc):
    qubits = qc.qubits()
    qc << Y(qubits[4]).control(qubits[0:4])
    return qc
