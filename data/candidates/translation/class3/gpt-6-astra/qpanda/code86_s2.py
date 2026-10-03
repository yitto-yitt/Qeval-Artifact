# EVAL_META: task_id=86, framework=qpanda, class=3
from pyqpanda3.core import QProg, QCircuit, H, CNOT


def collect_linear_blocks_with_and_without_limit():
    circuits = []

    for max_block_width in (None, 3):
        program = QProg()
        program << H(0)

        block = QCircuit()
        block_qubits = set()

        for control, target in ((0, 1), (1, 2), (2, 3), (3, 4)):
            next_qubits = block_qubits | {control, target}

            if max_block_width is not None and len(next_qubits) > max_block_width:
                program << block
                block = QCircuit()
                block_qubits = set()

            block << CNOT(control, target)
            block_qubits.update((control, target))

        if block_qubits:
            program << block

        circuits.append(program)

    return circuits[0], circuits[1]
