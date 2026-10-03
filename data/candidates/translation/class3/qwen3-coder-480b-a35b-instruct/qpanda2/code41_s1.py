# EVAL_META: task_id=41, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)

def compose_op():
    # Create 3-qubit identity operator (2^3 x 2^3 identity matrix)
    identity_matrix = np.eye(2**3, dtype=complex)
    
    # Create YX operator - Y on first qubit, X on second qubit
    # For YX on qubits [0, 2]: Y on qubit 0, X on qubit 2
    y_matrix = np.array([[0, -1j], [1j, 0]], dtype=complex)  # Y gate matrix
    x_matrix = np.array([[0, 1], [1, 0]], dtype=complex)     # X gate matrix
    
    # Tensor product Y ⊗ I ⊗ X (for qubits 0 and 2)
    temp = np.kron(y_matrix, x_matrix)
    yx_matrix = np.kron(temp, np.eye(2))  # Add identity for middle qubit
    
    # Since we need to apply Y on qubit 0 and X on qubit 2, we need to properly arrange the tensor product
    # The full operator acting on 3 qubits where Y acts on qubit 0 and X acts on qubit 2
    # Identity on qubit 1
    y_on_0 = y_matrix
    x_on_2 = x_matrix
    i_on_1 = np.eye(2)
    
    # To create Y on qubit 0 and X on qubit 2, we need to construct the full 8x8 matrix
    # We'll build it by considering all computational basis states
    full_yx_matrix = np.zeros((8, 8), dtype=complex)
    
    for i in range(8):
        # Convert i to 3-bit binary representation
        b = format(i, '03b')
        # b[0] corresponds to qubit 0, b[1] to qubit 1, b[2] to qubit 2
        q0 = int(b[0])
        q1 = int(b[1]) 
        q2 = int(b[2])
        
        # Apply Y to qubit 0 (flip bit 0 with phase if needed)
        new_q0 = 1 - q0  # Y flips the qubit state
        y_phase = (-1j)**q0 * 1j**(1-q0)  # Y matrix elements cause phase change
        
        # Apply X to qubit 2 (flip bit 2)
        new_q2 = 1 - q2
        
        # Keep qubit 1 unchanged
        new_q1 = q1
        
        new_index = (new_q0 << 2) | (new_q1 << 1) | new_q2
        full_yx_matrix[new_index, i] = y_phase * 1.0  # X doesn't add phase when flipping
    
    # Now compose: identity.compose(YX on [0,2]) with front=True means YX @ identity = YX
    # Actually, let's follow the original logic more directly in pyQPanda terms
    # We want to create the operator that applies Y to qubit 0 and X to qubit 2 while leaving qubit 1 alone
    
    # In pyQPanda, we can use the matrix representation directly
    op_identity = pq.QVec()
    for qubit in qubits:
        op_identity.append(qubit)
        
    # Create the composed operator
    # The operator representing Y on qubit 0 and X on qubit 2
    # This is equivalent to tensor product: Y(0) ⊗ I(1) ⊗ X(2)
    # But we need to represent it in the full 3-qubit space correctly
    
    # For the composition with front=True, we want to apply YX first then identity
    # Which effectively just gives us the YX operator since identity doesn't change anything
    # But the qargs specify where to apply YX: on qubits [0, 2]
    
    # Let's manually construct the matrix that represents applying Y to qubit 0 and X to qubit 2
    # When qargs=[0,2], it means Y operates on current qubit 0, X operates on current qubit 2
    # So we map the 4x4 YX operator to act on our 3-qubit system's qubits 0 and 2
    
    # Build the 8x8 matrix for Y on qubit 0 and X on qubit 2
    final_matrix = np.zeros((8, 8), dtype=complex)
    
    for src in range(8):  # Source computational basis state
        src_bits = [(src >> i) & 1 for i in range(3)]  # 3 bits [q2, q1, q0]
        src_q0, src_q1, src_q2 = src_bits[2], src_bits[1], src_bits[0]  # q0 is LSB
        
        # Apply Y to q0: |q0> -> sum(Y[q0', q0] * |q0'>)
        # Apply X to q2: |q2> -> |1-q2>
        # q1 remains unchanged
        
        # For Y gate: Y|0> = i|1>, Y|1> = -i|0>
        # So Y matrix: [[0, -i], [i, 0]]
        for new_q0 in range(2):
            y_amp = complex(0, -1j if src_q0 == 0 and new_q0 == 1 else (1j if src_q0 == 1 and new_q0 == 0 else 0))
            if y_amp != 0:
                new_q2 = 1 - src_q2  # X flips q2
                new_q1 = src_q1      # Identity on q1
                
                dest = (new_q2 << 2) | (new_q1 << 1) | new_q0
                final_matrix[dest, src] = y_amp * 1.0  # X contributes factor of 1 when flipping
    
    # In pyQPanda, we might need to create an operator from this matrix
    # However, pyQPanda has different approach - let's use quantum circuit to define the operation
    # and then get its unitary
    
    # Create a quantum circuit that applies X to qubit 2 and Y to qubit 0
    prog = pq.QProg()
    prog.insert(pq.RY(qubits[0], np.pi/2)).insert(pq.RZ(qubits[0], np.pi)).insert(pq.X(qubits[2]))
    # Actually Y gate can be decomposed as RZ(pi)*RY(pi) up to global phase, but standard Y is:
    # Y = [[0, -i], [i, 0]] which is implemented as RY(pi)RZ(pi) or similar
    
    # Better way: Y gate is available directly in some forms, or use the proper decomposition
    # Y gate: pq.Y(qubits[0]) would be ideal if available
    prog.clear()
    prog.insert(pq.U3(qubits[0], np.pi, np.pi/2, np.pi/2)).insert(pq.X(qubits[2]))  # U3 for Y gate
    
    # Get the unitary matrix of this program
    unitary = pq.get_unitary_matrix(prog, qubits)
    
    return unitary

result = compose_op()
machine.finalize()
