# EVAL_META: task_id=105, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QProg, CNOT, T

def initialize_cnot_dihedral():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    prog = QProg()
    prog << CNOT(qubits[0], qubits[1]) << T(qubits[0])
    qvm.directly_run(prog)
    return prog
