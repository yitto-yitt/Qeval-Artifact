# EVAL_META: task_id=86, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QProg, QCircuit, H, CNOT

def collect_linear_blocks_with_and_without_limit():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(5)
    circuit_full = QProg()
    circuit_full << H(qubits[0]) << CNOT(qubits[0], qubits[1]) << CNOT(qubits[1], qubits[2]) << CNOT(qubits[2], qubits[3]) << CNOT(qubits[3], qubits[4])
    circuit_limited = QProg()
    circuit_limited << H(qubits[0])
    block1 = QCircuit()
    block1 << CNOT(qubits[0], qubits[1]) << CNOT(qubits[1], qubits[2])
    circuit_limited << block1
    block2 = QCircuit()
    block2 << CNOT(qubits[2], qubits[3]) << CNOT(qubits[3], qubits[4])
    circuit_limited << block2
    qvm.finalize()
    return circuit_full, circuit_limited
