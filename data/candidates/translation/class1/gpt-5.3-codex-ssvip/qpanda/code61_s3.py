# EVAL_META: task_id=61, framework=qpanda, class=1
from pyqpanda3.core import QProg, measure_all


def create_quantum_circuit_with_one_qubit_and_measure():
    q = [0]
    c = [0]
    prog = QProg()
    prog << measure_all(q, c)
    return prog
