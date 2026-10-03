# EVAL_META: task_id=41, framework=qiskit, class=3
from qiskit.quantum_info import Operator, Pauli

def compose_op():
    yx_op = Operator(Pauli('YX'))
    id3 = Operator(Pauli('III'))
    return id3.compose(yx_op, qargs=[0,2])
