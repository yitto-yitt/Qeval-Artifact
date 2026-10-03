# EVAL_META: task_id=86, framework=qpanda2, class=3
import atexit
from pyqpanda import CPUQVM, QCircuit, H, CNOT

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(5)
atexit.register(machine.finalize)

def collect_linear_blocks_with_and_without_limit():
    full_block = QCircuit()
    full_linear = QCircuit()
    full_linear << CNOT(q[0], q[1])
    full_linear << CNOT(q[1], q[2])
    full_linear << CNOT(q[2], q[3])
    full_linear << CNOT(q[3], q[4])
    full_block << H(q[0])
    full_block << full_linear

    limited_block = QCircuit()
    limited_linear_1 = QCircuit()
    limited_linear_1 << CNOT(q[0], q[1])
    limited_linear_1 << CNOT(q[1], q[2])
    limited_linear_2 = QCircuit()
    limited_linear_2 << CNOT(q[2], q[3])
    limited_linear_2 << CNOT(q[3], q[4])
    limited_block << H(q[0])
    limited_block << limited_linear_1
    limited_block << limited_linear_2

    return full_block, limited_block
