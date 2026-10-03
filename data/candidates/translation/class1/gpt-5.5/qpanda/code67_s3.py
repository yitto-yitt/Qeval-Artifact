# EVAL_META: task_id=67, framework=qpanda, class=1
from math import pi
import pyqpanda3.core as pq


def chsh_circuit(alice, bob):
    machine = pq.CPUQVM()
    for name in ("init_qvm", "init", "initQVM"):
        if hasattr(machine, name):
            getattr(machine, name)()
            break

    for name in ("qAlloc_many", "qalloc_many", "qAllocMany", "qallocMany"):
        if hasattr(machine, name):
            q = getattr(machine, name)(2)
            break
    else:
        q = pq.qAlloc_many(2)

    for name in ("cAlloc_many", "calloc_many", "cAllocMany", "callocMany"):
        if hasattr(machine, name):
            c = getattr(machine, name)(2)
            break
    else:
        c = pq.cAlloc_many(2)

    prog = pq.QProg()

    h_gate = getattr(pq, "H")
    cnot_gate = getattr(pq, "CNOT") if hasattr(pq, "CNOT") else getattr(pq, "CX")
    ry_gate = getattr(pq, "RY")

    prog << h_gate(q[0])
    prog << cnot_gate(q[0], q[1])

    for name in ("BARRIER", "Barrier", "barrier"):
        if hasattr(pq, name):
            try:
                prog << getattr(pq, name)(q)
            except TypeError:
                pass
            break

    alice_angle = 0 if alice == 0 else -pi / 2
    try:
        prog << ry_gate(q[0], alice_angle)
    except TypeError:
        prog << ry_gate(alice_angle, q[0])

    measure_gate = getattr(pq, "Measure") if hasattr(pq, "Measure") else getattr(pq, "measure")
    prog << measure_gate(q[0], c[0])

    bob_angle = -pi / 4 if bob == 0 else pi / 4
    try:
        prog << ry_gate(q[1], bob_angle)
    except TypeError:
        prog << ry_gate(bob_angle, q[1])

    prog << measure_gate(q[1], c[1])

    if not hasattr(chsh_circuit, "_machines"):
        chsh_circuit._machines = []
    chsh_circuit._machines.append(machine)

    return prog
