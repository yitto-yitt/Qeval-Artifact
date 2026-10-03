# EVAL_META: task_id=105, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QProg, CNOT, T


def initialize_cnot_dihedral():
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(2)

    prog = QProg()
    prog << CNOT(q[0], q[1])
    prog << T(q[0])

    initialize_cnot_dihedral._machine = machine
    initialize_cnot_dihedral._qubits = q
    return prog
