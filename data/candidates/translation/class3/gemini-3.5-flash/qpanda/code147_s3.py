# EVAL_META: task_id=147, framework=qpanda, class=3
from pyqpanda3.core import Y, get_global_machine

def mcy(qc):
    qvm = get_global_machine()
    qubits = qvm.get_allocate_qubits()
    ctrl_qubits = qubits[0:4]
    target_qubit = qubits[4]
    qc << Y(target_qubit).control(ctrl_qubits)
    return qc
