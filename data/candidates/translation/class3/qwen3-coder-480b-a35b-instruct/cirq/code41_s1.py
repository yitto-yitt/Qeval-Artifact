# EVAL_META: task_id=41, framework=cirq, class=3
import cirq
import numpy as np


def compose_op():
    # Create 3-qubit identity operator
    op = cirq.unitary(cirq.IdentityGate(num_qubits=3))
    
    # Create YX Pauli operator
    yx = cirq.unitary(cirq.PauliString({cirq.LineQubit(0): cirq.Y, cirq.LineQubit(1): cirq.X}))
    
    # Pad YX to 3 qubits by tensoring with identity on qubit 1
    yx_full = np.kron(np.kron(np.eye(2), yx), np.eye(2))
    
    # Compose with front=True means yx_full @ op
    result = np.dot(yx_full, op)
    
    return cirq.MatrixGate(result)
