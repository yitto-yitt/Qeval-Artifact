# EVAL_META: task_id=41, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)

def compose_op():
    # Create 3-qubit identity operator (2^3 x 2^3 matrix)
    identity_matrix = np.eye(2**3)
    
    # Create YX operator - Y on first qubit, X on second qubit
    # YX means apply X to second qubit and Y to first qubit
    # In pyQPanda, we need to build the matrix for YX operator
    # Y = [[0, -1j], [1j, 0]]
    # X = [[0, 1], [1, 0]]
    # YX = Y ⊗ X = [[0, 0, 0, -1j], [0, 0, 1j, 0], [0, -1j, 0, 0], [1j, 0, 0, 0]]
    
    # For 3 qubits with YX acting on qubits 0 and 2:
    # We need to create a 8x8 matrix where Y acts on qubit 0 and X acts on qubit 2
    
    # Build YX operator matrix for qubits 0 and 2
    # The full 8x8 matrix considering qubits 0 and 2 with YX operation
    Y = np.array([[0, -1j], [1j, 0]])
    X = np.array([[0, 1], [1, 0]])
    
    # Tensor product Y (qubit 0) ⊗ I (qubit 1) ⊗ X (qubit 2)
    # But we need to account for the proper ordering in 3-qubit system
    # YX on qubits [0, 2] means Y on qubit 0 and X on qubit 2
    YX_partial = np.kron(Y, X)  # This gives us 4x4 matrix for qubits 0 and 2 combined
    # Identity for the middle qubit (qubit 1)
    Id_middle = np.eye(2)
    # Full operator: Y (on qubit 0) ⊗ Id (on qubit 1) ⊗ X (on qubit 2)
    # But the order in the tensor product needs to match the qubit indexing
    # Since we want YX on qubits [0,2], the effective tensor structure is more complex
    # Let's build it manually based on how each computational basis state transforms
    
    # Actually, let's approach this differently - use pyqpanda's built-in functionality
    # Create quantum programs to represent these operations and get their matrices
    
    # For the composition, we'll create operators directly
    # Identity on 3 qubits
    id_op = pq.QVec()
    for i in range(3):
        id_op.append(qubits[i])
    
    # Create the operator for YX on qubits [0, 2]
    # Build the matrix representation of YX operation on specified qubits
    full_matrix = np.eye(2**3)  # Start with identity
    
    # Apply YX transformation on qubits 0 and 2
    # For each computational basis |abc> -> new value based on YX action
    # YX means: Y on qubit 0, X on qubit 2
    # So |abc> -> Y_on_a * Id_on_b * X_on_c
    
    # Create the composed operator matrix
    # The operator YX on qubits [0,2] in a 3-qubit system
    yx_matrix = np.zeros((8, 8), dtype=complex)
    
    # Define Y and X matrices
    Y_matrix = np.array([[0, -1j], [1j, 0]], dtype=complex)
    X_matrix = np.array([[0, 1], [1, 0]], dtype=complex)
    
    # Fill the YX matrix on qubits 0 and 2
    for i in range(8):  # 8 basis states for 3 qubits
        # Convert i to binary to get |a b c>
        c_bit = i & 1          # least significant bit (qubit 2)
        b_bit = (i >> 1) & 1   # middle bit (qubit 1) 
        a_bit = (i >> 2) & 1   # most significant bit (qubit 0)
        
        # Apply Y to qubit 0 (a_bit) and X to qubit 2 (c_bit)
        # Y|a> and X|c>
        for out_a in range(2):
            for out_c in range(2):
                # Matrix element from input |a b c> to output |out_a b out_c>
                input_state_idx = i  # corresponds to |a b c>
                output_state_idx = (out_a << 2) | (b_bit << 1) | out_c  # |out_a b out_c>
                
                # Get matrix elements
                y_elem = Y_matrix[out_a, a_bit]
                x_elem = X_matrix[out_c, c_bit]
                
                # For identity on middle qubit, the b_bit stays the same
                if b_bit == ((output_state_idx >> 1) & 1):
                    yx_matrix[output_state_idx, input_state_idx] += y_elem * x_elem
                # If b_bit doesn't match, the element remains 0 (identity constraint)
    
    # Now compose the operators
    # In pyqpanda, we can work with matrices directly
    # Create a quantum program that represents this operator
    prog = pq.QProg()
    
    # For this specific case, let's create the composed operator directly
    # Using pyqpanda's operator functions
    
    # Since pyQPanda doesn't have direct operator composition like Qiskit,
    # we need to construct the final matrix manually based on the composition
    # op.compose(yx, qargs=[0, 2], front=True)
    # This means applying YX after the identity, which is just YX itself since identity doesn't change anything
    # But the qargs=[0,2] means YX acts on qubits 0 and 2 specifically
    
    # Actually, the identity composed with YX on qargs [0,2] front=True
    # means we apply YX first on specified qubits then identity (which does nothing)
    # So result is effectively YX applied to qubits [0,2] of a 3-qubit system
    
    # Return the matrix representation of the composed operator
    return yx_matrix

result = compose_op()
machine.finalize()
