# EVAL_META: task_id=67, framework=qpanda, class=1
from numpy import pi
from pyqpanda3.core import *


def chsh_circuit(alice, bob):
    cnot_gate = globals().get("CNOT") or globals().get("CX")
    measure_gate = globals().get("Measure") or globals().get("measure")

    def build(prog, q0, q1, c0, c1):
        prog = prog << H(q0)
        prog = prog << cnot_gate(q0, q1)
        if alice == 0:
            prog = prog << RY(q0, 0)
        else:
            prog = prog << RY(q0, -pi / 2)
        prog = prog << measure_gate(q0, c0)
        if bob == 0:
            prog = prog << RY(q1, -pi / 4)
        else:
            prog = prog << RY(q1, pi / 4)
        prog = prog << measure_gate(q1, c1)
        return prog

    for constructor in (
        lambda: QProg(),
        lambda: QProg(2),
        lambda: QProg(2, 2),
        lambda: QCircuit(2, 2),
        lambda: QCircuit(2),
        lambda: QCircuit(),
    ):
        try:
            return build(constructor(), 0, 1, 0, 1)
        except Exception:
            pass

    machine = CPUQVM()
    for init_name in ("init_qvm", "init"):
        if hasattr(machine, init_name):
            getattr(machine, init_name)()
            break

    try:
        q = machine.qAlloc_many(2)
    except Exception:
        try:
            q = machine.qalloc_many(2)
        except Exception:
            q = [machine.qAlloc(), machine.qAlloc()]

    try:
        c = machine.cAlloc_many(2)
    except Exception:
        try:
            c = machine.calloc_many(2)
        except Exception:
            c = [machine.cAlloc(), machine.cAlloc()]

    prog = build(QProg(), q[0], q[1], c[0], c[1])
    if not hasattr(chsh_circuit, "_machines"):
        chsh_circuit._machines = []
    chsh_circuit._machines.append(machine)
    return prog
