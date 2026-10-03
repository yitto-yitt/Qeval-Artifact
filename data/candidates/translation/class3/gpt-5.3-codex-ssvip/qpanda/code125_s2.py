# EVAL_META: task_id=125, framework=qpanda, class=3
from pyqpanda3.core import matrix_decompose


def circ_to_gate(circ):
    return matrix_decompose(circ.get_qv(), circ.get_matrix())
