# EVAL_META: task_id=67, framework=qpanda, class=1
from numpy import pi
from pyqpanda3.core import CPUQVM, QProg, H, CNOT, RY, Measure


def chsh_circuit(alice, bob):
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    cbits = qvm.cAlloc_many(2)
    prog = QProg()
    prog << H(qubits[0]) << CNOT(qubits[0], qubits[1])
    if alice == 0:
        prog << RY(qubits[0], 0)
    else:
        prog << RY(qubits[0], -pi / 2)
    prog << Measure(qubits[0], cbits[0])
    if bob == 0:
        prog << RY(qubits[1], -pi / 4)
    else:
        prog << RY(qubits[1], pi / 4)
    prog << Measure(qubits[1], cbits[1])
    return prog
