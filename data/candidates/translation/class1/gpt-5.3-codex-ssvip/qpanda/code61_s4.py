# EVAL_META: task_id=61, framework=qpanda, class=1
from pyqpanda3.core import *

def create_quantum_circuit_with_one_qubit_and_measure():
    q = qAlloc_many(1)
    c = cAlloc_many(1)
    prog = QProg()
    prog.insert(Measure(q[0], c[0]))
    return prog
