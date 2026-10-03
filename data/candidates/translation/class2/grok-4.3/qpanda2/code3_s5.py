# EVAL_META: task_id=3, framework=qpanda2, class=2
from pyqpanda import *
def create_ghz(drawing=False):
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(3)
    cbits = qvm.cAlloc_many(3)
    prog = QProg()
    prog << H(qubits[0]) << CNOT(qubits[0], qubits[1]) << CNOT(qubits[0], qubits[2])
    prog << Measure(qubits[0], cbits[0]) << Measure(qubits[1], cbits[1]) << Measure(qubits[2], cbits[2])
    if drawing:
        return prog, draw_qprog(prog)
    return prog
