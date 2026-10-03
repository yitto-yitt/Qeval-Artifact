# EVAL_META: task_id=41, framework=qiskit, class=3
from qiskit.quantum_info import Operator, Pauli


def compose_op():
    identity = Operator(Pauli('III'))
    yx = Operator(Pauli('YX'))
    return identity.compose(yx, qargs=[0, 2])
