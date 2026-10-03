# EVAL_META: task_id=41, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)

def compose_op():
    # Create 3-qubit identity operator
    identity_matrix = np.eye(2**3)
    
    # Create YX operator (Y on first qubit, X on second qubit)
    # For YX on qubits 0 and 2, we need to create appropriate matrix
    # Y = [[0, -1j], [1j, 0]], X = [[0, 1], [1, 0]]
    # So Y tensor X = [[0, 0, 0, -1j], [0, 0, 1j, 0], [0, -1j, 0, 0], [1j, 0, 0, 0]]
    y_matrix = np.array([[0, -1j], [1j, 0]])
    x_matrix = np.array([[0, 1], [1, 0]])
    
    # Tensor product Y ⊗ X
    yx_matrix = np.kron(y_matrix, x_matrix)  # This gives us a 4x4 matrix
    
    # To apply this to qubits 0 and 2 in a 3-qubit system, we need to expand appropriately
    # Identity for qubit 1: I
    i_matrix = np.eye(2)
    
    # For qargs=[0,2], we need to construct the full operator
    # We want Y on qubit 0, I on qubit 1, X on qubit 2 -> Y ⊗ I ⊗ X
    full_yix_matrix = np.kron(np.kron(y_matrix, i_matrix), x_matrix)
    
    # Since we're doing front=True composition, we apply YX first then identity
    # But since identity doesn't change anything, it's just the YX operation on specified qubits
    # Actually, let's think about this differently based on the Qiskit behavior
    
    # In Qiskit, when composing with qargs=[0, 2] on a 3-qubit identity,
    # it applies the 2-qubit operator YX to qubits 0 and 2 of the 3-qubit system
    # So we need to create a 3-qubit operator where Y acts on qubit 0 and X acts on qubit 2
    
    # Build the full 3-qubit operator matrix
    # For each computational basis state |abc> where a,b,c are bits:
    # |abc> -> Y_0|a> * I_1|b> * X_2|c>
    # So |000> -> Y|0> * |0> * X|0> = (-i|1>) * |0> * |1> = -i|101>
    # etc.
    
    # Construct the 8x8 matrix for Y on qubit 0 and X on qubit 2
    full_matrix = np.zeros((8, 8), dtype=complex)
    
    for i in range(8):
        # Convert i to binary representation for 3 qubits
        c2 = (i >> 2) & 1  # qubit 2
        c1 = (i >> 1) & 1  # qubit 1  
        c0 = i & 1         # qubit 0
        
        # Apply Y to qubit 0 (c0): |c0> -> sum(Y[c0, k0] * |k0>)
        # Apply I to qubit 1 (c1): |c1> -> |c1>
        # Apply X to qubit 2 (c2): |c2> -> |1-c2>
        
        # After X on qubit 2: new_c2 = 1 - c2
        new_c2 = 1 - c2
        # After I on qubit 1: new_c1 = c1
        new_c1 = c1
        # After Y on qubit 0: |c0> -> Y|c0>
        if c0 == 0:
            # Y|0> = -1j|1>
            new_c0 = 1
            coeff = -1j
        else:  # c0 == 1
            # Y|1> = 1j|0>
            new_c0 = 0
            coeff = 1j
            
        new_state = (new_c2 << 2) + (new_c1 << 1) + new_c0
        full_matrix[new_state, i] = coeff
    
    # Now compose: identity.compose(yx, qargs=[0,2], front=True)
    # This means apply yx first then identity, but identity doesn't change anything
    # So the result is just the operator that applies Y to qubit 0 and X to qubit 2
    return full_matrix

result = compose_op()
machine.finalize()
