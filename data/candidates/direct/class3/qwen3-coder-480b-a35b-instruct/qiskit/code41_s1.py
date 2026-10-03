# EVAL_META: task_id=41, framework=qiskit, class=3
from qiskit.quantum_info import Pauli, Operator
import numpy as np

def compose_op():
    # Create Pauli 'YX' operator (Y on qubit 1, X on qubit 0)
    yx_pauli = Pauli('YX')
    yx_operator = Operator(yx_pauli)
    
    # Create 3-qubit identity operator
    identity_3q = Operator.from_label('III')
    
    # Compose YX with 3-qubit identity on qubits 0 and 2
    # This means we need to tensor YX with I on the appropriate qubits
    # YX acts on qubits 1 and 0, so we need to insert identity on qubit 2
    composed_op = identity_3q.compose(yx_operator.expand(Operator.from_label('I')), qargs=[0, 1, 2])
    
    return composed_op
