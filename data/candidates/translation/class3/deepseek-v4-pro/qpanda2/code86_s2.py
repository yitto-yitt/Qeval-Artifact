# EVAL_META: task_id=86, framework=qpanda2, class=3
import atexit
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(5)

def collect_linear_blocks_with_and_without_limit():
    pairs = [(0, 1), (1, 2), (2, 3), (3, 4)]

    def build(max_block_width):
        blocks = []
        current_block = []
        current_qubits = set()

        for ctrl, tgt in pairs:
            if (max_block_width is not None and current_block and
                    len(current_qubits | {ctrl, tgt}) > max_block_width):
                blocks.append(current_block)
                current_block = []
                current_qubits = set()

            current_block.append((ctrl, tgt))
            current_qubits.update((ctrl, tgt))

        if current_block:
            blocks.append(current_block)

        circuit = QCircuit()
        circuit << H(q[0])
        for block in blocks:
            block_circuit = QCircuit()
            for ctrl, tgt in block:
                block_circuit << CNOT(q[ctrl], q[tgt])
            circuit << block_circuit

        return circuit

    return build(None), build(3)


def _cleanup():
    machine.finalize()


atexit.register(_cleanup)
