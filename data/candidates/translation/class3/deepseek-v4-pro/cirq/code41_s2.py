# EVAL_META: task_id=41, framework=cirq, class=3
import numpy as np
import cirq


def compose_op():
    # Create a 3-qubit identity operator as a 8x8 matrix
    id_3 = np.eye(2**3, dtype=complex)
    # Create the YX Pauli operator on 2 qubits as a 4x4 matrix
    yx_2 = np.kron(cirq.unitary(cirq.Y), cirq.unitary(cirq.X))
    # In Qiskit, compose with front=True means the given operator is applied first.
    # qargs=[0, 2] means we tensor the YX operator onto qubits 0 and 2, with identity on qubit 1.
    # The ordering here: qubits (0, 2) → tensor product YX on 0,2 and I on 1.
    # The full operator is YX ⊗ I ⊗ ? No, qargs specifies positions in the full register: (q0, q1, q2)
    # So yx_2 acts on qubits 0 and 2, identity on qubit 1.
    # The full 8x8 operator acting on qubits 0,1,2 in standard ordering is:
    # We need to permute the subsystems to place yx_2 on positions 0 and 2.
    # A common approach: represent as tensor product with identity on missing qubit and then permute.
    # Simpler: use cirq to build the operation directly.
    q0, q1, q2 = cirq.LineQubit.range(3)
    # Define the YX operation on qubits 0 and 2
    yx_op = cirq.Y(q0) * cirq.X(q2)
    # Identity on qubit 1 is implicit (no operation), so full unitary is the tensor product
    # Apply yx_op first, then identity (which does nothing). Since front=True in Qiskit,
    # the composed operator is id_3 @ full_yx_unitary (because front=True means the new op is applied first).
    # Construct the full 8x8 unitary of yx_op
    full_yx_unitary = cirq.unitary(yx_op)
    # Compose: identity after YX? front=True means: new_op @ self (matrix multiplication).
    # Original Qiskit: op.compose(yx, qargs=[0,2], front=True) gives yx_on_0_2 ⊗ I_on_1 applied first, then identity.
    # So total unitary = id_3 @ (yx_on_0_2 ⊗ I_on_1).
    # Since id_3 is identity, result is just the unitary of yx_on_0_2 ⊗ I_on_1.
    # However, we'll compute exactly as Qiskit does.
    result_matrix = id_3 @ full_yx_unitary
    return result_matrix
