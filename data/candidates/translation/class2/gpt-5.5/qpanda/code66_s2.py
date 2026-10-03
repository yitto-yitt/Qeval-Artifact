# EVAL_META: task_id=66, framework=qpanda, class=2
from numpy import arccos, sqrt
from pyqpanda3.core import *


def w_state():
    theta = 2 * arccos(1 / sqrt(3))

    def add(container, op):
        try:
            container << op
            return container
        except Exception:
            container.insert(op)
            return container

    def make_circuit():
        for args in ((3,), ()):
            try:
                return QCircuit(*args)
            except Exception:
                pass
        raise RuntimeError("Unable to create QCircuit")

    def make_prog():
        for args in ((), (3, 3), (3,)):
            try:
                return QProg(*args)
            except Exception:
                pass
        raise RuntimeError("Unable to create QProg")

    def gate(names, *args):
        last_error = None
        for name in names:
            fn = globals().get(name)
            if fn is None:
                continue
            try:
                return fn(*args)
            except Exception as exc:
                last_error = exc
        if last_error is not None:
            raise last_error
        raise RuntimeError("Gate not found: " + str(names))

    def controlled_h(control, target):
        ch = globals().get("CH")
        if ch is not None:
            try:
                return ch(control, target)
            except Exception:
                pass
        h_gate = gate(("H",), target)
        for controls in ([control], (control,), control):
            try:
                return h_gate.control(controls)
            except Exception:
                pass
        raise RuntimeError("Unable to create controlled-H gate")

    def measure_op(q, c):
        for name in ("Measure", "measure"):
            fn = globals().get(name)
            if fn is not None:
                try:
                    return fn(q, c)
                except Exception:
                    pass
        raise RuntimeError("Unable to create measurement")

    def build(q, c):
        circuit = make_circuit()
        add(circuit, gate(("RY",), q[0], theta))
        add(circuit, controlled_h(q[0], q[1]))
        add(circuit, gate(("CNOT", "CX"), q[1], q[2]))
        add(circuit, gate(("CNOT", "CX"), q[0], q[1]))
        add(circuit, gate(("X",), q[0]))

        prog = make_prog()
        add(prog, circuit)
        add(prog, measure_op(q[0], c[0]))
        add(prog, measure_op(q[1], c[1]))
        add(prog, measure_op(q[2], c[2]))
        return prog

    try:
        return build([0, 1, 2], [0, 1, 2])
    except Exception:
        machine = CPUQVM()
        try:
            machine.init_qvm()
        except Exception:
            pass

        q = None
        c = None
        for method in ("qAlloc_many", "qalloc_many"):
            if hasattr(machine, method):
                try:
                    q = getattr(machine, method)(3)
                    break
                except Exception:
                    pass
        if q is None and globals().get("qAlloc_many") is not None:
            q = qAlloc_many(3)

        for method in ("cAlloc_many", "calloc_many"):
            if hasattr(machine, method):
                try:
                    c = getattr(machine, method)(3)
                    break
                except Exception:
                    pass
        if c is None and globals().get("cAlloc_many") is not None:
            c = cAlloc_many(3)

        prog = build(q, c)
        try:
            prog._qvm = machine
        except Exception:
            pass
        return prog
