# EVAL_META: task_id=59, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)

def create_cz_gate():
    prog = QProg()
    prog << H(qubits[1]) << CNOT(qubits[0], qubits[1]) << H(qubits[1])
    return prog

machine.finalize()
