# EVAL_META: task_id=86, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def collect_linear_blocks_with_and_without_limit():
    def cnot_chain_unitary(num_wires):
        dim = 2 ** num_wires
        mat = np.zeros((dim, dim), dtype=complex)

        for col in range(dim):
            bits = [(col >> (num_wires - 1 - i)) & 1 for i in range(num_wires)]

            for i in range(num_wires - 1):
                bits[i + 1] ^= bits[i]

            row = 0
            for bit in bits:
                row = (row << 1) | bit

            mat[row, col] = 1.0

        return mat

    full_block = qml.tape.QuantumScript(
        [
            qml.Hadamard(wires=0),
            qml.QubitUnitary(cnot_chain_unitary(5), wires=[0, 1, 2, 3, 4], id="linear_function"),
        ]
    )

    limited_block = qml.tape.QuantumScript(
        [
            qml.Hadamard(wires=0),
            qml.QubitUnitary(cnot_chain_unitary(3), wires=[0, 1, 2], id="linear_function"),
            qml.QubitUnitary(cnot_chain_unitary(3), wires=[2, 3, 4], id="linear_function"),
        ]
    )

    return full_block, limited_block
