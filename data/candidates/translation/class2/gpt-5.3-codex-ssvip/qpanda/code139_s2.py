# EVAL_META: task_id=139, framework=qpanda, class=2
import numpy as np
from pyqpanda3.core import density_operator


def schmidt_test(data, qargs_B):
    rho = density_operator(np.array(data, dtype=complex))
    terms = rho.schmidt_decomposition(qargs_B)
    return [(term[0], term[1], term[2]) for term in terms]
