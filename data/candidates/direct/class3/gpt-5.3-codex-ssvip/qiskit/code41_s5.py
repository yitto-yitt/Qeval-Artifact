# EVAL_META: task_id=41, framework=qiskit, class=3
from qiskit.quantum_info import Operator, Pauli


def compose_op():
    id3 = Operator.from_label("III")
    yx_on_02 = Operator(Pauli("YIX"))
    return yx_on_02.compose(id3)
