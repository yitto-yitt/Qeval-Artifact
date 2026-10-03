# EVAL_META: task_id=41, framework=qpanda2, class=3
import numpy as np
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(3)

_prog = QProg()
_prog << X(q[0]) << I(q[1]) << Y(q[2])
_composed_op = np.array(get_matrix(_prog), dtype=complex)


def compose_op():
    return _composed_op


machine.finalize()
