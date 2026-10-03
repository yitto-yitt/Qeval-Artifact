# EVAL_META: task_id=41, framework=qiskit, class=3
from qiskit.quantum_info import Operator, Pauli


def compose_op():
    identity_3 = Operator.from_label("III")
    yx_on_02 = Operator(Pauli("YX")).expand(Operator.from_label("I"))
    return yx_on_02.compose(identity_3)
