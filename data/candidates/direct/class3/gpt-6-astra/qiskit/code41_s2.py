# EVAL_META: task_id=41, framework=qiskit, class=3
import numpy as np
from qiskit.quantum_info import Operator, Pauli


def compose_op():
    identity = Operator(np.eye(8, dtype=complex))
    return identity.compose(Operator(Pauli("YX")), qargs=[0, 2])
