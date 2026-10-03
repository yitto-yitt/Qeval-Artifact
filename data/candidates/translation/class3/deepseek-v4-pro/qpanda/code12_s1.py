# EVAL_META: task_id=12, framework=qpanda, class=3
from pyqpanda3.core import H, CNOT, qAlloc, QProg, get_unitary_matrix

def get_unitary():
    qubits = qAlloc(2)
    prog = QProg()
    prog << H(qubits[0]) << CNOT(qubits[0], qubits[1])
    return get_unitary_matrix(prog, qubits)
