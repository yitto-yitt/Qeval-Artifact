# EVAL_META: task_id=86, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def collect_linear_blocks_with_and_without_limit():
    def linear_block(cnot_chain, wires):
        mat = np.eye(2 ** len(wires), dtype=complex)
        for control, target in cnot_chain:
            mat = qml.matrix(qml.CNOT(wires=[control, target]), wire_order=wires) @ mat
        return qml.QubitUnitary(mat, wires=wires)

    full_block = qml.tape.QuantumScript(
        ops=[
            qml.Hadamard(wires=0),
            linear_block([(0, 1), (1, 2), (2, 3), (3, 4)], wires=[0, 1, 2, 3, 4]),
        ],
        measurements=[],
    )

    limited_block = qml.tape.QuantumScript(
        ops=[
            qml.Hadamard(wires=0),
            linear_block([(0, 1), (1, 2)], wires=[0, 1, 2]),
            linear_block([(2, 3), (3, 4)], wires=[2, 3, 4]),
        ],
        measurements=[],
    )

    return full_block, limited_block
