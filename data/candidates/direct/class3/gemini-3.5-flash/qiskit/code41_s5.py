# EVAL_META: task_id=41, framework=qiskit, class=3
from qiskit.quantum_info import Operator, Pauli

def compose_op():
    identity = Operator(Pauli('III'))
    yx_pauli = Pauli('YX')
    return identity.compose(yx_pauli, qargs=[0, 2])
