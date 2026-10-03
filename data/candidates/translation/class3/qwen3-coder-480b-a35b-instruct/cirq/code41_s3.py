# EVAL_META: task_id=41, framework=cirq, class=3
import cirq
import numpy as np


def compose_op():
    # Create a 3-qubit identity operator
    op = cirq.IdentityGate(num_qubits=3)
    
    # Create YX operator - Y on first qubit, X on second qubit
    yx_op = cirq.kron(cirq.Y, cirq.X)
    
    # To compose YX with identity on qubits 0 and 2, we need to create the full operator
    # Identity on qubit 1, Y on qubit 0, X on qubit 2 -> kron(I, Y, X) but arranged properly
    
    # Build the composed operator manually by considering the action on each qubit
    # We want YX to act on qubits 0 and 2 (front=True means YX acts first)
    # So we have: I on qubit 1, Y on qubit 0, X on qubit 2
    qubits = [cirq.LineQubit(0), cirq.LineQubit(1), cirq.LineQubit(2)]
    
    # Create the full operator matrix for YX acting on qubits 0 and 2
    # This is equivalent to I ⊗ Y ⊗ X (but in the right order for our qubit arrangement)
    yx_full = cirq.kron(cirq.unitary(cirq.Y), cirq.unitary(cirq.X), cirq.unitary(cirq.I))
    
    # Actually, let's build this more systematically
    # For 3 qubits, we want Y on qubit 0, X on qubit 2, I on qubit 1
    # The operator should be Y_0 ⊗ I_1 ⊗ X_2 rearranged appropriately
    
    # Build the full 8x8 matrix for the operator that applies Y to qubit 0 and X to qubit 2
    # while leaving qubit 1 unchanged
    y_matrix = cirq.unitary(cirq.Y)
    x_matrix = cirq.unitary(cirq.X)
    i_matrix = cirq.unitary(cirq.I)
    
    # Create the full operator by tensoring appropriately
    # We want Y on qubit 0, I on qubit 1, X on qubit 2
    full_op_matrix = cirq.kron(y_matrix, i_matrix, x_matrix)
    
    # But we need to account for the actual qubit ordering in the computational basis
    # The operator that acts as Y on qubit 0 and X on qubit 2 is:
    # sum over all |b0,b1,b2><b0,b1,b2| where b0,b1,b2 are bit values
    # Y_0 ⊗ I_1 ⊗ X_2 would be kron(Y, I, X) but we need to be careful about bit ordering
    
    # Let's construct it directly by considering how it acts on basis states
    # For 3 qubits, we have |q0,q1,q2> and we want Y on q0, X on q2
    # So |q0,q1,q2> -> (Y|q0>) ⊗ |q1> ⊗ (X|q2>)
    
    # The full 8x8 matrix can be built by taking kronecker products in the right order
    # Since we're using standard ordering where qubit 0 is the least significant bit,
    # the operator Y on qubit 0 and X on qubit 2 is kron(X, I, Y) in terms of kron product
    # Wait, let me reconsider the bit ordering in Cirq
    
    # In Cirq, if we have qubits [q0, q1, q2], then a state is |q0>⊗|q1>⊗|q2>
    # So to apply Y to q0 and X to q2, we need Y⊗I⊗X
    yx_on_02 = cirq.kron(y_matrix, i_matrix, x_matrix)
    
    # Now compose with identity (which is just the 8x8 identity matrix)
    identity_3q = np.eye(8)
    
    # Since front=True means YX acts first, then identity
    # But identity doesn't change anything, so result is just the YX operator
    # Actually, we need to return an operator that represents the composition
    composed_matrix = np.dot(identity_3q, yx_on_02)  # Identity doesn't change it
    
    return cirq.DensePauliString('Y_I_X').on(*[cirq.LineQubit(i) for i in range(3)])
