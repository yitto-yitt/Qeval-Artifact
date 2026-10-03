# EVAL_META: task_id=61, framework=qpanda, class=1
from pyqpanda3.core import *


def create_quantum_circuit_with_one_qubit_and_measure():
    q = qalloc(1)
    c = calloc(1)
    prog = QProg()
    prog.insert(measure_all(q, c))
    return prog
