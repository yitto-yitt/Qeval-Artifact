# EVAL_META: task_id=66, framework=qpanda, class=2
from numpy import arccos, sqrt
from pyqpanda3.core import CPUQVM, QProg, RY, H, CNOT, X, Measure


def w_state():
    machine = CPUQVM()
    machine.init()
    qubits = machine.qAlloc_many(3)
    cbits = machine.cAlloc_many(3)

    prog = QProg()
    prog << RY(qubits[0], 2 * arccos(1 / sqrt(3)))
    prog << H(qubits[1]).control([qubits[0]])
    prog << CNOT(qubits[1], qubits[2])
    prog << CNOT(qubits[0], qubits[1])
    prog << X(qubits[0])
    prog << Measure(qubits[0], cbits[0])
    prog << Measure(qubits[1], cbits[1])
    prog << Measure(qubits[2], cbits[2])
    return prog
