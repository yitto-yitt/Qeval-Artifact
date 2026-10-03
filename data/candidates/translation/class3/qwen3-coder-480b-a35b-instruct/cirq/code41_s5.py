# EVAL_META: task_id=41, framework=cirq, class=3
import cirq
import numpy as np


def compose_op():
    # Create a 3-qubit identity operator
    identity_op = cirq.IdentityGate(num_qubits=3)
    
    # Create YX operator (Y on first qubit, X on second qubit)
    yx_op = cirq.kron(cirq.Y, cirq.X)
    
    # To compose YX with identity on qubits 0 and 2, we need to create the full operator
    # Identity on qubit 1, Y on qubit 0, X on qubit 2 -> I ⊗ Y ⊗ X ordering
    full_op = cirq.kron(cirq.I, cirq.Y, cirq.X)  # This applies Y to qubit 1, X to qubit 2 if using standard kron
    
    # Actually, let's think about this differently
    # We want to apply Y to qubit 0 and X to qubit 2 of a 3-qubit system
    # So we need: Y ⊗ I ⊗ X (in terms of action on computational basis)
    op1 = cirq.Y.on(cirq.LineQubit(0))
    op2 = cirq.X.on(cirq.LineQubit(2))
    
    # Create the combined operation
    yx_on_0_2 = cirq.kron_with_identity(cirq.Y, 1) @ cirq.kron(cirq.I, cirq.X)
    # Actually, let's build it properly
    qubits = [cirq.LineQubit(i) for i in range(3)]
    y_on_0 = cirq.Y(qubits[0])
    x_on_2 = cirq.X(qubits[2])
    
    # Create dense matrices and compose them
    y_matrix = cirq.unitary(y_on_0)
    x_matrix = cirq.unitary(x_on_2)
    identity_matrix = cirq.unitary(cirq.I(qubits[1]))
    
    # Build the full operator: Y(0) ⊗ I(1) ⊗ X(2)
    yx_full = cirq.kron(y_matrix, cirq.unitary(cirq.I), x_matrix)
    
    # The identity operator for 3 qubits
    identity_3q = cirq.unitary(cirq.IdentityGate(3))
    
    # Compose: identity.compose(yx_full) with front=True means yx_full @ identity
    result_matrix = yx_full @ identity_3q
    
    return cirq.DensePauliString(result_matrix)
