# EVAL_META: task_id=86, framework=pennylane, class=3
import pennylane as qml

def collect_linear_blocks_with_and_without_limit():
    # Full block: no width restriction
    with qml.tape.QuantumTape() as full_tape:
        qml.Hadamard(wires=0)
        with qml.tape.QuantumTape() as chain_tape:
            qml.CNOT(wires=[0, 1])
            qml.CNOT(wires=[1, 2])
            qml.CNOT(wires=[2, 3])
            qml.CNOT(wires=[3, 4])
        mat_full = qml.matrix(chain_tape, wire_order=[0, 1, 2, 3, 4])
        qml.QubitUnitary(mat_full, wires=[0, 1, 2, 3, 4])

    # Limited block: max_block_width=3
    with qml.tape.QuantumTape() as limited_tape:
        qml.Hadamard(wires=0)
        with qml.tape.QuantumTape() as block1_tape:
            qml.CNOT(wires=[0, 1])
            qml.CNOT(wires=[1, 2])
        mat_block1 = qml.matrix(block1_tape, wire_order=[0, 1, 2])
        qml.QubitUnitary(mat_block1, wires=[0, 1, 2])
        with qml.tape.QuantumTape() as block2_tape:
            qml.CNOT(wires=[2, 3])
            qml.CNOT(wires=[3, 4])
        mat_block2 = qml.matrix(block2_tape, wire_order=[2, 3, 4])
        qml.QubitUnitary(mat_block2, wires=[2, 3, 4])

    return full_tape, limited_tape
