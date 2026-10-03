# EVAL_META: task_id=105, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QProg, CNOT, T


def initialize_cnot_dihedral():
    qvm = CPUQVM()
    if hasattr(qvm, "init_qvm"):
        qvm.init_qvm()
    elif hasattr(qvm, "init"):
        qvm.init()

    qubits = qvm.qAlloc_many(2)

    prog = QProg()
    prog << CNOT(qubits[0], qubits[1])
    prog << T(qubits[0])

    initialize_cnot_dihedral._qvm = qvm
    initialize_cnot_dihedral._qubits = qubits

    return prog
