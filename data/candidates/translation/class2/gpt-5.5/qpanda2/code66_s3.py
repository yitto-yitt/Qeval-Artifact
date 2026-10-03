# EVAL_META: task_id=66, framework=qpanda2, class=2
from math import acos, sqrt, pi
import pyqpanda as pq


def w_state():
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(3)
    cbits = machine.cAlloc_many(3)

    prog = pq.QProg()
    prog << pq.RY(qubits[0], 2 * acos(1 / sqrt(3)))
    prog << pq.RY(qubits[1], pi / 4)
    prog << pq.CNOT(qubits[0], qubits[1])
    prog << pq.RY(qubits[1], -pi / 4)
    prog << pq.CNOT(qubits[0], qubits[1])
    prog << pq.CNOT(qubits[1], qubits[2])
    prog << pq.CNOT(qubits[0], qubits[1])
    prog << pq.X(qubits[0])
    prog << pq.Measure(qubits[0], cbits[0])
    prog << pq.Measure(qubits[1], cbits[1])
    prog << pq.Measure(qubits[2], cbits[2])

    w_state._machine = machine
    w_state._qubits = qubits
    w_state._cbits = cbits
    return prog
