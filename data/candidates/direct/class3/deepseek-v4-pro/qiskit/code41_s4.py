# EVAL_META: task_id=41, framework=qiskit, class=3
import numpy as np
from qiskit.quantum_info import Operator, Pauli

def compose_op():
    yx = Operator(Pauli('YX'))
    identity_3q = Operator(np.eye(8))
    return identity_3q.compose(yx, qargs=[0, 2])
