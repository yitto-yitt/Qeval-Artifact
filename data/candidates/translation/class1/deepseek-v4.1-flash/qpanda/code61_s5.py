# EVAL_META: task_id=61, framework=qpanda, class=1
from pyqpanda3.core import QProg, Qubit, CBit, measure


def create_quantum_circuit_with_one_qubit_and_measure():
    q = Qubit(1)
    c = CBit(1)
    prog = QProg()
    prog << measure(q[0], c[0])
    return prog
