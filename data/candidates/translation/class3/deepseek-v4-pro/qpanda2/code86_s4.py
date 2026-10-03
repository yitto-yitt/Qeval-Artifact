# EVAL_META: task_id=86, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(5)

def collect_linear_blocks_with_and_without_limit():
    full_block = QCircuit()
    full_block << H(q[0])
    linear_full = QCircuit()
    linear_full << CNOT(q[0], q[1]) << CNOT(q[1], q[2]) << CNOT(q[2], q[3]) << CNOT(q[3], q[4])
    full_block << linear_full

    limited_block = QCircuit()
    limited_block << H(q[0])
    linear_limited_1 = QCircuit()
    linear_limited_1 << CNOT(q[0], q[1]) << CNOT(q[1], q[2])
    limited_block << linear_limited_1
    linear_limited_2 = QCircuit()
    linear_limited_2 << CNOT(q[2], q[3]) << CNOT(q[3], q[4])
    limited_block << linear_limited_2

    return full_block, limited_block

machine.finalize()
