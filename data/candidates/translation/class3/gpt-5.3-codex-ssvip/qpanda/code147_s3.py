# EVAL_META: task_id=147, framework=qpanda, class=3
from pyqpanda3.core import Y, QVec

def mcy(qc):
    qubits = qc.get_used_qubits()
    controls = QVec()
    controls.push_back(qubits[0])
    controls.push_back(qubits[1])
    controls.push_back(qubits[2])
    controls.push_back(qubits[3])
    qc << Y(qubits[4]).control(controls)
    return qc
