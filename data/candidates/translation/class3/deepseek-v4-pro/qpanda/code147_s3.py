# EVAL_META: task_id=147, framework=qpanda, class=3
from pyqpanda3.core import Y

def mcy(qc):
    mcy_gate = Y(qc.qubits[4]).control(qc.qubits[0:4])
    qc.append(mcy_gate)
    return qc
