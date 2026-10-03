# EVAL_META: task_id=61, framework=qpanda, class=1
from pyqpanda3.core import QCircuit, QProg, measure


def create_quantum_circuit_with_one_qubit_and_measure():
    prog = QProg()
    prog << measure(0, 0)
    return prog
