# EVAL_META: task_id=41, framework=qiskit, class=3
from qiskit.quantum_info import Operator, Pauli

def compose_op():
    id_op = Operator.from_label('III')
    yx_op = Operator(Pauli('YX'))
    return id_op.compose(yx_op, qargs=[0, 2])
