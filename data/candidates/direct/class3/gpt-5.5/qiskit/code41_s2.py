# EVAL_META: task_id=41, framework=qiskit, class=3
import numpy as np
from qiskit.quantum_info import Operator, Pauli


def compose_op():
    identity_3q = Operator(np.eye(8))
    yx_op = Operator(Pauli("YX"))
    return identity_3q.compose(yx_op, qargs=[0, 2])
