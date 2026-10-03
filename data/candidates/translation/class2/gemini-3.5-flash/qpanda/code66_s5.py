# EVAL_META: task_id=66, framework=qpanda, class=2
from numpy import arccos, sqrt
from pyqpanda3.core import CH, CNOT, RY, X, CPUQVM, Measure, QProg

qvm = CPUQVM()
qvm.init_qvm()


def w_state():
    qubits = qvm.qAlloc_many(3)
    cbits = qvm.cAlloc_many(3)

    prog = QProg()
    prog << RY(qubits[0], 2 * arccos(1 / sqrt(3)))
    prog << CH(qubits[0], qubits[1])
    prog << CNOT(qubits[1], qubits[2])
    prog << CNOT(qubits[0], qubits[1])
    prog << X(qubits[0])

    for i in range(3):
        prog << Measure(qubits[i], cbits[i])

    return prog
