# EVAL_META: task_id=86, framework=pennylane, class=3
import pennylane as qml
import numpy as np
from pennylane.tape import QuantumScript

def collect_linear_blocks_with_and_without_limit():
    def cx_unitary_n(control, target, n):
        dim = 2**n
        U = np.eye(dim, dtype=complex)
        for i in range(dim):
            control_bit = (i >> (n - 1 - control)) & 1
            if control_bit:
                new_i = i ^ (1 << (n - 1 - target))
                U[new_i, i] = 1
                U[i, i] = 0
        return U

    # Full block: all 4 CX gates collected into one LinearFunction on qubits 0-4
    U_cx01 = cx_unitary_n(0, 1, 5)
    U_cx12 = cx_unitary_n(1, 2, 5)
    U_cx23 = cx_unitary_n(2, 3, 5)
    U_cx34 = cx_unitary_n(3, 4, 5)
    U_full = U_cx34 @ U_cx23 @ U_cx12 @ U_cx01

    # Limited block: max width 3 -> two blocks
    # First block: CX(0,1) then CX(1,2) on qubits 0,1,2
    U1_cx01 = cx_unitary_n(0, 1, 3)
    U1_cx12 = cx_unitary_n(1, 2, 3)
    U_first = U1_cx12 @ U1_cx01

    # Second block: CX(2,3) then CX(3,4) on qubits 2,3,4 -> local 0,1,2
    U2_cx01 = cx_unitary_n(0, 1, 3)
    U2_cx12 = cx_unitary_n(1, 2, 3)
    U_second = U2_cx12 @ U2_cx01

    full_ops = [
        qml.Hadamard(wires=0),
        qml.QubitUnitary(U_full, wires=[0, 1, 2, 3, 4])
    ]
    full_tape = QuantumScript(full_ops)

    limited_ops = [
        qml.Hadamard(wires=0),
        qml.QubitUnitary(U_first, wires=[0, 1, 2]),
        qml.QubitUnitary(U_second, wires=[2, 3, 4])
    ]
    limited_tape = QuantumScript(limited_ops)

    return full_tape, limited_tape
