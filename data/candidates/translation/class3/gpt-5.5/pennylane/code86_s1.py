# EVAL_META: task_id=86, framework=pennylane, class=3
import pennylane as qml
import numpy as np


def collect_linear_blocks_with_and_without_limit():
    def cnot_chain_matrix(num_wires, cnots):
        dim = 2**num_wires
        mat = np.zeros((dim, dim), dtype=complex)
        for col in range(dim):
            bits = [(col >> (num_wires - 1 - i)) & 1 for i in range(num_wires)]
            for control, target in cnots:
                if bits[control]:
                    bits[target] ^= 1
            row = 0
            for bit in bits:
                row = (row << 1) | bit
            mat[row, col] = 1.0
        return mat

    full_linear = cnot_chain_matrix(5, [(0, 1), (1, 2), (2, 3), (3, 4)])
    limited_linear_1 = cnot_chain_matrix(3, [(0, 1), (1, 2)])
    limited_linear_2 = cnot_chain_matrix(3, [(0, 1), (1, 2)])

    full_block = qml.tape.QuantumScript(
        [
            qml.Hadamard(wires=0),
            qml.QubitUnitary(full_linear, wires=[0, 1, 2, 3, 4], unitary_check=False),
        ]
    )

    limited_block = qml.tape.QuantumScript(
        [
            qml.Hadamard(wires=0),
            qml.QubitUnitary(limited_linear_1, wires=[0, 1, 2], unitary_check=False),
            qml.QubitUnitary(limited_linear_2, wires=[2, 3, 4], unitary_check=False),
        ]
    )

    return full_block, limited_block
