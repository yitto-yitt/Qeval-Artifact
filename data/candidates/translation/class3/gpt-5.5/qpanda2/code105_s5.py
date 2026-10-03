# EVAL_META: task_id=105, framework=qpanda2, class=3
import atexit
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)
atexit.register(machine.finalize)


def initialize_cnot_dihedral():
    prog = QProg()
    prog << CNOT(qubits[0], qubits[1])
    prog << T(qubits[0])
    return prog
