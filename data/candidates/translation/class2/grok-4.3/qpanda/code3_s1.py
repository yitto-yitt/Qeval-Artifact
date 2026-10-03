# EVAL_META: task_id=3, framework=qpanda, class=2
from pyqpanda3.core import *

def create_ghz(drawing=False):
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(3)
    cbits = qvm.cAlloc_many(3)
    prog = QProg()
    prog << H(qubits[0]) << CNOT(qubits[0], qubits[1]) << CNOT(qubits[0], qubits[2])
    for i in range(3):
        prog << Measure(qubits[i], cbits[i])
    if drawing:
        return prog, draw_qprog(prog)
    return prog
