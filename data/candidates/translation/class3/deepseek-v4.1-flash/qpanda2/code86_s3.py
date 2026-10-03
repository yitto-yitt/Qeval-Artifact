# EVAL_META: task_id=86, framework=qpanda2, class=3
from pyqpanda import *

qvm = CPUQVM()
qvm.init_qvm()
qubits = qvm.qAlloc_many(5)

def collect_linear_blocks_with_and_without_limit():
    # Full block: entire CX chain as a single linear function block
    full_block = QProg()
    full_block << H(qubits[0])
    cx_chain = QCircuit()
    cx_chain << CNOT(qubits[0], qubits[1])
    cx_chain << CNOT(qubits[1], qubits[2])
    cx_chain << CNOT(qubits[2], qubits[3])
    cx_chain << CNOT(qubits[3], qubits[4])
    full_block << cx_chain

    # Limited block: max_block_width=3, split into two blocks
    limited_block = QProg()
    limited_block << H(qubits[0])
    block1 = QCircuit()
    block1 << CNOT(qubits[0], qubits[1])
    block1 << CNOT(qubits[1], qubits[2])
    limited_block << block1
    block2 = QCircuit()
    block2 << CNOT(qubits[2], qubits[3])
    block2 << CNOT(qubits[3], qubits[4])
    limited_block << block2

    return full_block, limited_block

qvm.finalize()
