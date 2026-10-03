# EVAL_META: task_id=41, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)


def compose_op():
    prog = QProg()
    prog << X(qubits[0]) << Y(qubits[2])
    mat = machine.get_matrix(prog, qubits)
    return QOperator(mat, qubits)


machine.finalize()
