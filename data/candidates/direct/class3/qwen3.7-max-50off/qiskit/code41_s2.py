# EVAL_META: task_id=41, framework=qiskit, class=3
from qiskit.quantum_info import Operator, Pauli

def compose_op():
    yx = Pauli('YX')
    id_op = Operator.from_label('III')
    return id_op.compose(Operator(yx), qargs=[0, 2])
