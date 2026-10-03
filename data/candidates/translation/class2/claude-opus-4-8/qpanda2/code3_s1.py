# EVAL_META: task_id=3, framework=qpanda2, class=2
from pyqpanda import *


def create_ghz(drawing=False):
    machine = CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(3)
    cbits = machine.cAlloc_many(3)

    prog = QProg()
    prog << H(qubits[0])
    prog << CNOT(qubits[0], qubits[1])
    prog << CNOT(qubits[0], qubits[2])
    prog << Measure(qubits[0], cbits[0])
    prog << Measure(qubits[1], cbits[1])
    prog << Measure(qubits[2], cbits[2])

    if drawing:
        fig = draw_qprog(prog, output="mpl")
        return prog, fig
    return prog
