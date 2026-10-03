# EVAL_META: task_id=86, framework=qpanda, class=3
from pyqpanda3.core import QProg, QCircuit, H, CNOT


def collect_linear_blocks_with_and_without_limit():
    linear_gates = [(0, 1), (1, 2), (2, 3), (3, 4)]

    def collect(max_block_width=None):
        program = QProg()
        program << H(0)

        block = QCircuit()
        block_qubits = set()

        for control, target in linear_gates:
            gate_qubits = {control, target}
            if (
                max_block_width is not None
                and len(block_qubits | gate_qubits) > max_block_width
            ):
                program << block
                block = QCircuit()
                block_qubits = set()

            block << CNOT(control, target)
            block_qubits.update(gate_qubits)

        if block_qubits:
            program << block

        return program

    return collect(), collect(max_block_width=3)
