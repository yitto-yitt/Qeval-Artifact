# EVAL_META: task_id=147, framework=qpanda, class=3
from pyqpanda3.core import *

def mcy(qc):
    qubits = qc.get_qubits()
    qc << Y(qubits[4]).control([qubits[0], qubits[1], qubits[2], qubits[3]])
    return qc
