# EVAL_META: task_id=6, framework=qpanda, class=2
from pyqpanda3.core import QProg, X

def create_state_prep(num_qubits):
    prog = QProg()
    prog << X(0)
    return prog
