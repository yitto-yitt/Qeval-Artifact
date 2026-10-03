# EVAL_META: task_id=105, framework=qpanda, class=3
from pyqpanda import *
from pyqpanda.core import *


def initialize_cnot_dihedral():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    prog = QProg()
    prog.insert(CNOT(qubits[0], qubits[1]))
    prog.insert(T(qubits[0]))
    return prog
