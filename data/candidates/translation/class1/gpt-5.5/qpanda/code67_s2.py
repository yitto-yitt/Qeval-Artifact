# EVAL_META: task_id=67, framework=qpanda, class=1
from math import pi
import pyqpanda3.core as pq


def chsh_circuit(alice, bob):
    machine = pq.CPUQVM()
    init = getattr(machine, "init_qvm", None) or getattr(machine, "init", None)
    if init is not None:
        init()

    qalloc = getattr(machine, "qAlloc_many", None) or getattr(machine, "qalloc_many")
    calloc = getattr(machine, "cAlloc_many", None) or getattr(machine, "calloc_many")
    q = qalloc(2)
    c = calloc(2)

    prog = pq.QProg()
    measure = getattr(pq, "Measure", None) or getattr(pq, "measure", None)
    cnot = getattr(pq, "CNOT", None) or getattr(pq, "CX")

    def _ry(qubit, angle):
        try:
            return pq.RY(qubit, angle)
        except TypeError:
            return pq.RY(angle, qubit)

    def _measure(qubit, cbit):
        try:
            return measure(qubit, cbit)
        except TypeError:
            return measure(cbit, qubit)

    prog << pq.H(q[0])
    prog << cnot(q[0], q[1])

    if alice == 0:
        prog << _ry(q[0], 0)
    else:
        prog << _ry(q[0], -pi / 2)
    prog << _measure(q[0], c[0])

    if bob == 0:
        prog << _ry(q[1], -pi / 4)
    else:
        prog << _ry(q[1], pi / 4)
    prog << _measure(q[1], c[1])

    holders = getattr(chsh_circuit, "_qpanda_holders", None)
    if holders is None:
        holders = []
        chsh_circuit._qpanda_holders = holders
    holders.append((machine, q, c))

    return prog
