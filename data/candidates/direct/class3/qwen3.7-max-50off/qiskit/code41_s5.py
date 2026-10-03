# EVAL_META: task_id=41, framework=qiskit, class=3
from qiskit.quantum_info import Operator, Pauli

def compose_op():
    yx = Pauli('YX')
    ident = Operator.from_label('III')
    return ident.compose(yx, qargs=[0, 2])
