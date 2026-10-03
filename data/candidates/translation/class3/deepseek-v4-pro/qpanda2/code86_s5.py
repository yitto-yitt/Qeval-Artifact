# EVAL_META: task_id=86, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.initQVM()
q = machine.qAlloc_many(5)

def collect_linear_blocks_with_and_without_limit():
    full_linear_block = QCircuit()
    full_linear_block << CNOT(q[0], q[1]) << CNOT(q[1], q[2]) << CNOT(q[2], q[3]) << CNOT(q[3], q[4])
    full_circuit = QCircuit()
    full_circuit << H(q[0]) << full_linear_block

    block1 = QCircuit()
    block1 << CNOT(q[0], q[1]) << CNOT(q[1], q[2])
    block2 = QCircuit()
    block2 << CNOT(q[2], q[3]) << CNOT(q[3], q[4])
    limited_circuit = QCircuit()
    limited_circuit << H(q[0]) << block1 << block2

    return full_circuit, limited_circuit

machine.finalize()
