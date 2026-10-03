# EVAL_META: task_id=66, framework=qpanda2, class=2
from numpy import arccos, sqrt
from pyqpanda import *


def w_state():
    machine = init_quantum_machine(QMachineType.CPU)
    qubits = machine.qAlloc_many(3)
    cbits = machine.cAlloc_many(3)

    prog = QProg()
    prog << RY(qubits[0], 2 * arccos(1 / sqrt(3)))
    prog << H(qubits[1]).control([qubits[0]])
    prog << CNOT(qubits[1], qubits[2])
    prog << CNOT(qubits[0], qubits[1])
    prog << X(qubits[0])
    prog << measure_all(qubits, cbits)

    return prog
