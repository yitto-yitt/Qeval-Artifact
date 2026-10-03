# EVAL_META: task_id=105, framework=qpanda2, class=3
from pyqpanda import CPUQVM, qAlloc_many, QProg, CNOT, T

machine = CPUQVM()
machine.init_qvm()
qubits = qAlloc_many(2)

def initialize_cnot_dihedral():
    prog = QProg()
    prog << CNOT(qubits[0], qubits[1])
    prog << T(qubits[0])
    return prog

machine.finalize()
