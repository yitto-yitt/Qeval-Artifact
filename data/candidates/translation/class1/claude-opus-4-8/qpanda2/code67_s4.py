# EVAL_META: task_id=67, framework=qpanda2, class=1
from numpy import pi
import pyqpanda as pq


def chsh_circuit(alice, bob):
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    cbits = qvm.cAlloc_many(2)

    prog = pq.QProg()
    prog << pq.H(qubits[0])
    prog << pq.CNOT(qubits[0], qubits[1])
    prog << pq.BARRIER(qubits)

    if alice == 0:
        prog << pq.RY(qubits[0], 0)
    else:
        prog << pq.RY(qubits[0], -pi / 2)
    prog << pq.Measure(qubits[0], cbits[0])

    if bob == 0:
        prog << pq.RY(qubits[1], -pi / 4)
    else:
        prog << pq.RY(qubits[1], pi / 4)
    prog << pq.Measure(qubits[1], cbits[1])

    return prog
