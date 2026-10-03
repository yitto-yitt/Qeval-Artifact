# EVAL_META: task_id=86, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, CNOT, QOracle

def collect_linear_blocks_with_and_without_limit():
    M5 = [
        [1, 0, 0, 0, 0],
        [1, 1, 0, 0, 0],
        [1, 1, 1, 0, 0],
        [1, 1, 1, 1, 0],
        [1, 1, 1, 1, 1]
    ]
    full_block = QCircuit()
    full_block << H(0)
    full_block << QOracle(M5, [0, 1, 2, 3, 4])

    M3 = [
        [1, 0, 0],
        [1, 1, 0],
        [1, 1, 1]
    ]
    limited_block = QCircuit()
    limited_block << H(0)
    limited_block << QOracle(M3, [0, 1, 2])
    limited_block << QOracle(M3, [2, 3, 4])

    return full_block, limited_block
