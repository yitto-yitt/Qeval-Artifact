# EVAL_META: task_id=41, framework=qiskit, class=3
import numpy as np
from qiskit.quantum_info import Operator, Pauli

def compose_op():
    yx = Pauli('YX')
    id_op = Operator(np.eye(8))
    return id_op.compose(yx, qubits=[0, 2])
