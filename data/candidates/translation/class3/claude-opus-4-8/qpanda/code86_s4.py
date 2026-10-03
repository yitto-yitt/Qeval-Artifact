# EVAL_META: task_id=86, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QProg, H, CNOT


def collect_linear_blocks_with_and_without_limit():
    def build_full():
        circ = QCircuit(5)
        circ << H(0)
        circ << CNOT(0, 1)
        circ << CNOT(1, 2)
        circ << CNOT(2, 3)
        circ << CNOT(3, 4)
        prog = QProg()
        prog << circ
        return prog

    def build_limited():
        block1 = QCircuit(5)
        block1 << H(0)
        block1 << CNOT(0, 1)
        block1 << CNOT(1, 2)

        block2 = QCircuit(5)
        block2 << CNOT(2, 3)
        block2 << CNOT(3, 4)

        prog = QProg()
        prog << block1
        prog << block2
        return prog

    full_block = build_full()
    limited_block = build_limited()
    return full_block, limited_block
