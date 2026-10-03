# EVAL_META: task_id=86, framework=qpanda2, class=3
from pyqpanda import *
machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(5)
def collect_linear_blocks_with_and_without_limit():
    qc_full = QCircuit()
    qc_full << H(qubits[0]) << CNOT(qubits[0], qubits[1]) << CNOT(qubits[1], qubits[2]) << CNOT(qubits[2], qubits[3]) << CNOT(qubits[3], qubits[4])
    prog_full = QProg()
    prog_full << qc_full
    qc_limited1 = QCircuit()
    qc_limited1 << H(qubits[0]) << CNOT(qubits[0], qubits[1]) << CNOT(qubits[1], qubits[2])
    qc_limited2 = QCircuit()
    qc_limited2 << CNOT(qubits[2], qubits[3]) << CNOT(qubits[3], qubits[4])
    prog_limited = QProg()
    prog_limited << qc_limited1 << qc_limited2
    return prog_full, prog_limited
machine.finalize()
