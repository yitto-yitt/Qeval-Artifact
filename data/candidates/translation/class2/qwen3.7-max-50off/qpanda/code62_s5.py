# EVAL_META: task_id=62, framework=qpanda, class=2
from pyqpanda3.core import QProg, QVec, X, H

def bb84_senders_circuit(state, basis):
    num_qubits = len(state)
    qubits = QVec(num_qubits)
    prog = QProg()
    for i in range(len(basis)):
        if state[i] == 1:
            prog << X(qubits[i])
        if basis[i] == 1:
            prog << H(qubits[i])
    return prog
