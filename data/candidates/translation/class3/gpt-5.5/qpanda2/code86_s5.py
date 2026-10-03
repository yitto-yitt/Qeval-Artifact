# EVAL_META: task_id=86, framework=qpanda2, class=3
import atexit
from pyqpanda import CPUQVM, QCircuit, H, CNOT

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(5)
atexit.register(machine.finalize)

def collect_linear_blocks_with_and_without_limit():
    full_block = QCircuit()
    full_block << H(qubits[0])
    full_block << CNOT(qubits[0], qubits[1])
    full_block << CNOT(qubits[1], qubits[2])
    full_block << CNOT(qubits[2], qubits[3])
    full_block << CNOT(qubits[3], qubits[4])

    limited_block = QCircuit()
    limited_block << H(qubits[0])
    limited_block << CNOT(qubits[0], qubits[1])
    limited_block << CNOT(qubits[1], qubits[2])
    limited_block << CNOT(qubits[2], qubits[3])
    limited_block << CNOT(qubits[3], qubits[4])

    return full_block, limited_block
