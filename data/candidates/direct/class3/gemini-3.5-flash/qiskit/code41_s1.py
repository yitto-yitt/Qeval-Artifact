# EVAL_META: task_id=41, framework=qiskit, class=3
from qiskit.quantum_info import Operator, Pauli

def compose_op():
    identity = Operator.from_label('III')
    yx = Pauli('YX')
    return identity.compose(yx, qargs=[0, 2])
