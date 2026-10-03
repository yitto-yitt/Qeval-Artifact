# EVAL_META: task_id=86, framework=pennylane, class=3
import numpy as np
import pennylane as qml


def collect_linear_blocks_with_and_without_limit():
    def block_matrix(block_wires, pairs):
        dim = 2 ** len(block_wires)
        mat = np.eye(dim, dtype=complex)
        for control, target in pairs:
            gate = qml.matrix(
                qml.CNOT(wires=[control, target]), wire_order=block_wires
            )
            mat = gate @ mat
        return mat

    full_wires = [0, 1, 2, 3, 4]
    full_pairs = [(0, 1), (1, 2), (2, 3), (3, 4)]
    full_matrix = block_matrix(full_wires, full_pairs)
    full_tape = qml.tape.QuantumScript(
        [qml.Hadamard(wires=0), qml.QubitUnitary(full_matrix, wires=full_wires)],
        measurements=[],
    )

    block_1_wires = [0, 1, 2]
    block_1_pairs = [(0, 1), (1, 2)]
    block_1_matrix = block_matrix(block_1_wires, block_1_pairs)

    block_2_wires = [2, 3, 4]
    block_2_pairs = [(2, 3), (3, 4)]
    block_2_matrix = block_matrix(block_2_wires, block_2_pairs)

    limited_tape = qml.tape.QuantumScript(
        [
            qml.Hadamard(wires=0),
            qml.QubitUnitary(block_1_matrix, wires=block_1_wires),
            qml.QubitUnitary(block_2_matrix, wires=block_2_wires),
        ],
        measurements=[],
    )

    return full_tape, limited_tape
