# EVAL_META: task_id=41, framework=qiskit, class=3
from qiskit.quantum_info import Operator, Pauli

def compose_op():
    return Operator(Pauli('III')).compose(Operator(Pauli('YX')), qargs=[0, 2])
