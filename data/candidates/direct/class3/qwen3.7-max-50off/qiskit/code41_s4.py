# EVAL_META: task_id=41, framework=qiskit, class=3
from qiskit.quantum_info import Operator, Pauli

def compose_op():
    yx_op = Operator(Pauli('YX'))
    id_op = Operator(Pauli('III'))
    return id_op.compose(yx_op, qubits=[0, 2])
