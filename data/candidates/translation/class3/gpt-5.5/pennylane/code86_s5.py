# EVAL_META: task_id=86, framework=pennylane, class=3
import numpy as np
import pennylane as qml

def collect_linear_blocks_with_and_without_limit():
    def linear_unitary(num_wires, cnot_pairs):
        dim = 2 ** num_wires
        mat = np.zeros((dim, dim), dtype=complex)
        for col in range(dim):
            bits = [(col >> (num_wires - 1 - i)) & 1 for i in range(num_wires)]
            for control, target in cnot_pairs:
                if bits[control]:
                    bits[target] ^= 1
            row = 0
            for bit in bits:
                row = (row << 1) | bit
            mat[row, col] = 1.0
        return mat

    full_ops = [
        qml.Hadamard(wires=0),
        qml.QubitUnitary(
            linear_unitary(5, [(0, 1), (1, 2), (2, 3), (3, 4)]),
            wires=[0, 1, 2, 3, 4],
        ),
    ]

    limited_ops = [
        qml.Hadamard(wires=0),
        qml.QubitUnitary(linear_unitary(3, [(0, 1), (1, 2)]), wires=[0, 1, 2]),
        qml.QubitUnitary(linear_unitary(3, [(0, 1), (1, 2)]), wires=[2, 3, 4]),
    ]

    full_block = qml.tape.QuantumScript(full_ops)
    limited_block = qml.tape.QuantumScript(limited_ops)
    return full_block, limited_block
