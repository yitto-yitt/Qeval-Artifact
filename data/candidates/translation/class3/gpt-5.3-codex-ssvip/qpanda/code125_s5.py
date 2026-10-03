# EVAL_META: task_id=125, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QProg, matrix_decompose


def circ_to_gate(circ):
    if not isinstance(circ, QCircuit):
        raise TypeError("circ must be a pyqpanda3.core.QCircuit")
    prog = QProg()
    prog.insert(circ)
    return matrix_decompose(prog)
