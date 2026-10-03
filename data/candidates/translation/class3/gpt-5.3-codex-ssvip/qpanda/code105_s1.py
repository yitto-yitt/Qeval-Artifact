# EVAL_META: task_id=105, framework=qpanda, class=3
from pyqpanda3.core import *

def initialize_cnot_dihedral():
    machine = CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(2)

    prog = QProg()
    prog.insert(CNOT(qubits[0], qubits[1]))
    prog.insert(T(qubits[0]))

    unitary = get_unitary(prog, False)
    machine.finalize()
    return unitary
