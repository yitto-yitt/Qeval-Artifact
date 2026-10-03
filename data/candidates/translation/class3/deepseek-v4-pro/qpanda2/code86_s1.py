# EVAL_META: task_id=86, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.initQVM()
q = machine.qAlloc_many(5)

def collect_linear_blocks_with_and_without_limit():
    full = QCircuit()
    full << H(q[0])
    linear_full = QCircuit()
    linear_full << CNOT(q[0], q[1]) << CNOT(q[1], q[2]) << CNOT(q[2], q[3]) << CNOT(q[3], q[4])
    full << linear_full

    limited = QCircuit()
    limited << H(q[0])
    block1 = QCircuit()
    block1 << CNOT(q[0], q[1]) << CNOT(q[1], q[2])
    block2 = QCircuit()
    block2 << CNOT(q[2], q[3]) << CNOT(q[3], q[4])
    limited << block1 << block2

    return full, limited

machine.finalize()
