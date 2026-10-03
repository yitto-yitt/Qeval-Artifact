# EVAL_META: task_id=86, framework=pennylane, class=3
import pennylane as qml
from pennylane.tape import QuantumScript


def collect_linear_blocks_with_and_without_limit():
    def _linear_matrix(wires, cnot_sequence):
        ops = [qml.CNOT(wires=list(pair)) for pair in cnot_sequence]
        tape = QuantumScript(ops, measurements=[])
        return qml.matrix(tape, wire_order=list(wires))

    full_wires = [0, 1, 2, 3, 4]
    full_cnots = [(0, 1), (1, 2), (2, 3), (3, 4)]

    full_matrix = _linear_matrix(full_wires, full_cnots)
    full_block = QuantumScript(
        [
            qml.Hadamard(wires=0),
            qml.QubitUnitary(full_matrix, wires=full_wires),
        ],
        measurements=[],
    )

    block1_wires = [0, 1, 2]
    block1_cnots = [(0, 1), (1, 2)]
    block2_wires = [2, 3, 4]
    block2_cnots = [(2, 3), (3, 4)]

    block1_matrix = _linear_matrix(block1_wires, block1_cnots)
    block2_matrix = _linear_matrix(block2_wires, block2_cnots)

    limited_block = QuantumScript(
        [
            qml.Hadamard(wires=0),
            qml.QubitUnitary(block1_matrix, wires=block1_wires),
            qml.QubitUnitary(block2_matrix, wires=block2_wires),
        ],
        measurements=[],
    )

    return full_block, limited_block
