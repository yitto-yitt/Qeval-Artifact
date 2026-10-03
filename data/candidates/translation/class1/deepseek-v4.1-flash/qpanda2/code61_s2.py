# EVAL_META: task_id=61, framework=qpanda2, class=1
from pyqpanda import *


def create_quantum_circuit_with_one_qubit_and_measure():
    q = qAlloc()
    c = cAlloc()
    prog = QProg()
    prog << measure(q, c)
    return prog
