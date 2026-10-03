# EVAL_META: task_id=41, framework=qiskit, class=3
from qiskit.quantum_info import Operator, Pauli

def compose_op():
    id3 = Operator.from_label("III")
    yx = Operator(Pauli("YX"))
    return id3.compose(yx, qubits=[0, 2])
