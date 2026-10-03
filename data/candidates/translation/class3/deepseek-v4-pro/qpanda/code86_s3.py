# EVAL_META: task_id=86, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit, H, CNOT

def collect_linear_blocks_with_and_without_limit():
    full_block = QuantumCircuit(5)
    full_block << H(0)
    full_block << CNOT(0, 1)
    full_block << CNOT(1, 2)
    full_block << CNOT(2, 3)
    full_block << CNOT(3, 4)

    limited_block = QuantumCircuit(5)
    limited_block << H(0)
    limited_block << CNOT(0, 1)
    limited_block << CNOT(1, 2)
    limited_block << CNOT(2, 3)
    limited_block << CNOT(3, 4)

    return full_block, limited_block
