# EVAL_META: task_id=6, framework=qpanda, class=2
from pyqpanda3.core import QProg, X, I


def create_state_prep(num_qubits):
    prog = QProg()
    for qubit in range(num_qubits):
        prog << (X(qubit) if qubit == 0 else I(qubit))
    return prog
