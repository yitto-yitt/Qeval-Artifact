# EVAL_META: task_id=86, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QProg, QCircuit, H, CNOT


def collect_linear_blocks_with_and_without_limit():
    linear_block = QCircuit()
    for control in range(4):
        linear_block << CNOT(control, control + 1)

    full_block = QProg()
    full_block << H(0)
    full_block << linear_block

    first_block = QCircuit()
    first_block << CNOT(0, 1)
    first_block << CNOT(1, 2)

    second_block = QCircuit()
    second_block << CNOT(2, 3)
    second_block << CNOT(3, 4)

    limited_block = QProg()
    limited_block << H(0)
    limited_block << first_block
    limited_block << second_block

    simulator = CPUQVM()
    simulator.run(full_block, shots=1)
    simulator.run(limited_block, shots=1)

    return full_block, limited_block
