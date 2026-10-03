# EVAL_META: task_id=66, framework=qpanda, class=2
from numpy import arccos, sqrt
from pyqpanda3.core import CPUQVM, QProg, RY, H, CNOT, X, Measure


def w_state():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(3)
    cbits = qvm.cAlloc_many(3)
    prog = QProg()
    prog.insert(RY(qubits[0], 2 * arccos(1 / sqrt(3))))
    prog.insert(H(qubits[1]).control(qubits[0]))
    prog.insert(CNOT(qubits[1], qubits[2]))
    prog.insert(CNOT(qubits[0], qubits[1]))
    prog.insert(X(qubits[0]))
    for i in range(3):
        prog.insert(Measure(qubits[i], cbits[i]))
    return prog
