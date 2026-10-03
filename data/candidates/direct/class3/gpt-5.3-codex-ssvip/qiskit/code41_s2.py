# EVAL_META: task_id=41, framework=qiskit, class=3
from qiskit.quantum_info import Operator, Pauli


def compose_op():
    identity_3 = Operator.from_label("III")
    yx_on_02 = Pauli("YIX")
    return identity_3.compose(Operator(yx_on_02))
