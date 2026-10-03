# EVAL_META: task_id=57, framework=qpanda2, class=3
from pyqpanda import *

qvm = CPUQVM()
qvm.init_qvm()
qubits = qvm.qAlloc_many(2)

def create_swap_gate():
    prog = QProg()
    prog << CNOT(qubits[0], qubits[1])
    prog << CNOT(qubits[1], qubits[0])
    prog << CNOT(qubits[0], qubits[1])
    return prog

qvm.finalize()
