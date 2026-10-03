# EVAL_META: task_id=147, framework=qpanda, class=3
from pyqpanda3.core import Y, control

def mcy(qc):
    qubits = qc.get_used_qubits()
    gate = Y(qubits[4])
    qc.insert(control(gate, qubits[0:4]))
    return qc
