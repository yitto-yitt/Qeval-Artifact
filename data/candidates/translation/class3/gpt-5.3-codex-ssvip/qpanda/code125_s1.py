# EVAL_META: task_id=125, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QProg, matrix_decompose


def circ_to_gate(circ):
    prog = QProg()
    prog << circ
    return matrix_decompose(prog)
