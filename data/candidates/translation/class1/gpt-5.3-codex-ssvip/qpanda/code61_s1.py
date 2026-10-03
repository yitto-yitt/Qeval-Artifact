# EVAL_META: task_id=61, framework=qpanda, class=1
from pyqpanda3.core import QProg, Measure


def create_quantum_circuit_with_one_qubit_and_measure():
    prog = QProg()
    q = prog.qalloc(1, "q")
    c = prog.calloc(1, "c")
    prog.insert(Measure(q[0], c[0]))
    return prog
