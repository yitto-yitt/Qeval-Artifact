# EVAL_META: task_id=41, framework=qiskit, class=3
from qiskit.quantum_info import Operator, Pauli


def compose_op():
    identity_op = Operator.from_label("III")
    pauli_op = Operator(Pauli("YX"))
    return identity_op.compose(pauli_op, qargs=[0, 2])
