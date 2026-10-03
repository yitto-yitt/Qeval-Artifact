# EVAL_META: task_id=66, framework=qpanda, class=2
from numpy import arccos, sqrt, pi
import pyqpanda3.core as pq


def w_state():
    qvm = pq.CPUQVM()
    if hasattr(qvm, "init_qvm"):
        qvm.init_qvm()

    qubits = qvm.qAlloc_many(3)
    cbits = qvm.cAlloc_many(3)

    prog = pq.QProg()
    prog << pq.RY(qubits[0], 2 * arccos(1 / sqrt(3)))

    prog << pq.RY(qubits[1], pi / 4)
    prog << pq.H(qubits[1])
    prog << pq.CNOT(qubits[0], qubits[1])
    prog << pq.H(qubits[1])
    prog << pq.RY(qubits[1], -pi / 4)

    prog << pq.CNOT(qubits[1], qubits[2])
    prog << pq.CNOT(qubits[0], qubits[1])
    prog << pq.X(qubits[0])
    prog << pq.measure_all(qubits, cbits)

    return prog
