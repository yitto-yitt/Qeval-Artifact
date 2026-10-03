# EVAL_META: task_id=86, framework=qpanda2, class=3
from pyqpanda import CPUQVM, QCircuit, H, CNOT

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(5)

def collect_linear_blocks_with_and_without_limit():
    full_block = QCircuit()
    full_block << H(qubits[0])
    full_linear = QCircuit()
    full_linear << CNOT(qubits[0], qubits[1])
    full_linear << CNOT(qubits[1], qubits[2])
    full_linear << CNOT(qubits[2], qubits[3])
    full_linear << CNOT(qubits[3], qubits[4])
    full_block << full_linear

    limited_block = QCircuit()
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

machine.finalize()
