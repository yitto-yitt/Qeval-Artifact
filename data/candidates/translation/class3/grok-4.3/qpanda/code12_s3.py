# EVAL_META: task_id=12, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QProg, H, CNOT, get_unitary as get_unitary_matrix

def get_unitary():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    prog = QProg()
    prog << H(qubits[0]) << CNOT(qubits[0], qubits[1])
    unitary = get_unitary_matrix(qvm, prog)
    return unitary
