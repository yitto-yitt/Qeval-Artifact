# EVAL_META: task_id=41, framework=cirq, class=3
import cirq
import numpy as np


def compose_op():
    # Create a 3-qubit identity operator
    identity_op = cirq.IdentityGate(num_qubits=3)
    
    # Create YX operator - Y on qubit 0, X on qubit 1 (in the 2-qubit space)
    y_op = cirq.Y
    x_op = cirq.X
    
    # For composing on specific qubits, we need to create the full operator
    # YX on qubits 0 and 2 means Y on qubit 0 and X on qubit 2
    qubits = [cirq.LineQubit(i) for i in range(3)]
    
    # Identity operator for 3 qubits
    identity_matrix = np.eye(8)
    
    # YX operator on qubits 0 and 2
    yx_matrix = np.kron(cirq.unitary(cirq.Y), np.kron(np.eye(2), cirq.unitary(cirq.X)))
    
    # Rearrange to match qubit ordering: we want Y on qubit 0, X on qubit 2
    # So we need to tensor appropriately
    y_on_0 = cirq.Y(qubits[0])
    x_on_2 = cirq.X(qubits[2])
    
    # Create the composite operation
    yx_op = cirq.PauliString({qubits[0]: cirq.Y, qubits[2]: cirq.X})
    
    # Convert to dense matrix form for composition
    yx_unitary = cirq.unitary(yx_op)
    identity_unitary = cirq.unitary(cirq.I.on_each(*qubits))
    
    # To properly compose, we need to work with the full 8x8 matrices
    # Since we're working with 3 qubits, identity is 8x8
    # And YX on qubits 0,2 also needs to be represented as 8x8
    full_yx_matrix = np.eye(8)
    # Apply YX transformation
    y_matrix = cirq.unitary(cirq.Y)  # 2x2 Y matrix
    x_matrix = cirq.unitary(cirq.X)  # 2x2 X matrix
    
    # Build the full 8x8 matrix for Y on qubit 0 and X on qubit 2
    # We'll construct it by considering all basis states
    full_yx_matrix = np.zeros((8,8), dtype=complex)
    for i in range(8):
        # Convert i to binary representation for 3 qubits
        b = format(i, '03b')
        # Apply Y to bit 0 and X to bit 2
        new_b = ''
        new_b += str((int(b[0]) + 1) % 2) if b[0] == '0' else str((int(b[0]) + 1) % 2)  # Y flips and adds phase
        new_b += b[1]  # middle qubit unchanged
        new_b += str((int(b[2]) + 1) % 2)  # X flips
        
        # Y gate action: |0> -> i|1>, |1> -> -i|0>
        # X gate action: |0> -> |1>, |1> -> |0>
        
        # Actually build the proper unitary for Y on q0 and X on q2
    y_unitary = cirq.unitary(cirq.Y)  # [[0, -1j], [1j, 0]]
    x_unitary = cirq.unitary(cirq.X)  # [[0, 1], [1, 0]]
    
    # Construct the full operator: Y on qubit 0, I on qubit 1, X on qubit 2
    full_yx_op_matrix = np.kron(np.kron(y_unitary, np.eye(2)), x_unitary)
    
    # Reshape to match the right qubit order: we want Y on qubit 0, X on qubit 2, I on qubit 1
    # Need to permute the tensor product order
    full_yx_op_matrix = np.kron(y_unitary, np.kron(np.eye(2), x_unitary))
    # Actually, let's use the proper tensor construction
    op_identity = cirq.DensePauliString('III').on(*qubits)
    yx_pauli = cirq.DensePauliString('YIY').on(*qubits)  # This isn't right
    
    # Let me reconstruct properly
    q0, q1, q2 = cirq.LineQubit.range(3)
    yx_tensor = cirq.unitary(cirq.Y).reshape(2,2)
    temp = np.kron(yx_tensor, np.eye(2))  # Now 4x4, corresponds to YI
    final_yx = np.kron(temp, cirq.unitary(cirq.X)).reshape(8,8)  # Now YIX
    
    # Actually, we want Y on qubit 0 and X on qubit 2, so Y_I_X
    # kron(Y_0, I_1, X_2) gives us YIX, but we want YXI where Y is on first position and X on third
    # In terms of kron: kron(kron(Y, I), X) = YIX
    # But we want Y on q0 and X on q2, which means Y_I_X in terms of kron would be kron(Y, kron(I, X))
    # No, that's still not right. Let's think differently.
    
    # The correct way: we have qubits [q0, q1, q2]. We want Y on q0 and X on q2.
    # So our operator should be Y ⊗ I ⊗ X acting on the state space
    yx_full = np.kron(np.kron(cirq.unitary(cirq.Y), np.eye(2)), cirq.unitary(cirq.X))
    
    # The identity for 3 qubits
    identity_full = np.eye(8)
    
    # Compose them (with front=True meaning yx is applied first)
    result_matrix = np.dot(identity_full, yx_full)  # Since front=True, yx comes first in multiplication
    
    return cirq.DensePauliString(result_matrix)
    
    # Actually, let's use Cirq's built-in functionality more directly
    qubits = cirq.LineQubit.range(3)
    yx_op = cirq.PauliString([cirq.Y(qubits[0]), cirq.X(qubits[2])])
    identity_op = cirq.PauliString([cirq.I(qubits[0]), cirq.I(qubits[1]), cirq.I(qubits[2])])
    
    # Compose them
    composed = identity_op * yx_op  # This is equivalent to front=True composition
    return composed
