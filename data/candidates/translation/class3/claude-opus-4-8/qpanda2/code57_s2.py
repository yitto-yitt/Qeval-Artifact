# EVAL_META: task_id=57, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()

def create_swap_gate():
    qubits = machine.qAlloc_many(2)
    prog = QProg()
    prog << CNOT(qubits[0], qubits[1]) \
         << CNOT(qubits[1], qubits[0]) \
         << CNOT(qubits[0], qubits[1])
    return prog

machine.finalize()
