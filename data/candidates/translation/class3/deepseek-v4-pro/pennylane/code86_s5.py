# EVAL_META: task_id=86, framework=pennylane, class=3
import numpy as np
import pennylane as qml
from pennylane.tape import QuantumScript


def _linear_block_matrix(num_qubits, cnot_pairs):
    dim = 2 ** num_qubits
    matrix = np.zeros((dim, dim), dtype=np.complex128)

    for input_idx in range(dim):
        bits = [(input_idx >> i) & 1 for i in range(num_qubits)]
        for control, target in cnot_pairs:
            bits[target] ^= bits[control]
        output_idx = sum(bit << i for i, bit in enumerate(bits))
        matrix[output_idx, input_idx] = 1.0 + 0.0j

    return matrix


def collect_linear_blocks_with_and_without_limit():
    full_chain = [(0, 1), (1, 2), (2, 3), (3, 4)]
    full_matrix = _linear_block_matrix(5, full_chain)

    first_block_pairs = [(0, 1), (1, 2)]
    second_block_pairs = [(0, 1), (1, 2)]
    block1_matrix = _linear_block_matrix(3, first_block_pairs)
    block2_matrix = _linear_block_matrix(3, second_block_pairs)

    full_ops = [
        qml.Hadamard(0),
        qml.QubitUnitary(full_matrix, wires=[0, 1, 2, 3, 4]),
    ]

    limited_ops = [
        qml.Hadamard(0),
        qml.QubitUnitary(block1_matrix, wires=[0, 1, 2]),
        qml.QubitUnitary(block2_matrix, wires=[2, 3, 4]),
    ]

    full_block = QuantumScript(full_ops)
    limited_block = QuantumScript(limited_ops)

    return full_block, limited_block
