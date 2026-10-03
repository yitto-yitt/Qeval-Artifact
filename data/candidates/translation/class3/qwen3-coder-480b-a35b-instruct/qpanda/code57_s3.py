# EVAL_META: task_id=57, framework=qpanda, class=3
from pyqpanda3.core import *

def create_swap_gate():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    prog = QProg()
    prog << CNOT(qubits[0], qubits[1]) << CNOT(qubits[1], qubits[0]) << CNOT(qubits[0], qubits[1])
    return prog
