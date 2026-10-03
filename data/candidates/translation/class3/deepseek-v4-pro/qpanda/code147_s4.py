# EVAL_META: task_id=147, framework=qpanda, class=3
from pyqpanda3.core import Y

def mcy(qc):
    qubits = qc.qubits
    controls = [qubits[i] for i in range(4)]
    gate = Y(qubits[4]).control(controls)
    qc << gate
    return qc
