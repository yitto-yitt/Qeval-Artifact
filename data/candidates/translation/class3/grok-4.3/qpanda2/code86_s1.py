# EVAL_META: task_id=86, framework=qpanda2, class=3
from pyqpanda import *
machine = CPUQVM()
machine.initQVM()
qubits = machine.qAlloc_many(5)
def collect_linear_blocks_with_and_without_limit():
    full_prog = QProg()
    full_prog << H(qubits[0]) << CNOT(qubits[0], qubits[1]) << CNOT(qubits[1], qubits[2]) << CNOT(qubits[2], qubits[3]) << CNOT(qubits[3], qubits[4])
    limited_prog = QProg()
    limited_prog << H(qubits[0]) << CNOT(qubits[0], qubits[1]) << CNOT(qubits[1], qubits[2])
    limited_prog << CNOT(qubits[2], qubits[3]) << CNOT(qubits[3], qubits[4])
    machine.finalize()
    return full_prog, limited_prog
