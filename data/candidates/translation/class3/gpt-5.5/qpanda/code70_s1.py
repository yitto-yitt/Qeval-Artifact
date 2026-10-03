# EVAL_META: task_id=70, framework=qpanda, class=3
from pyqpanda3.core import *
import math

def create_quantum_circuit_based_h0_cswap012_h1_csdg10():
    def _init_machine():
        m = CPUQVM()
        for name in ("init_qvm", "init", "initQVM"):
            if hasattr(m, name):
                try:
                    getattr(m, name)()
                except TypeError:
                    pass
                break
        return m

    def _alloc_qubits(m, n):
        for name in ("qAlloc_many", "qalloc_many", "qAllocMany", "allocate_qubits"):
            if hasattr(m, name):
                return getattr(m, name)(n)
        return [m.qAlloc() for _ in range(n)]

    def _append(container, op):
        try:
            container << op
            return container
        except Exception:
            pass
        for name in ("insert", "append"):
            if hasattr(container, name):
                getattr(container, name)(op)
                return container
        raise RuntimeError("Cannot append operation to QProg")

    def _gate(names):
        for name in names:
            g = globals().get(name)
            if callable(g):
                return g
        raise RuntimeError("Required gate is unavailable")

    def _dagger(g):
        for name in ("dagger", "set_dagger", "setDagger"):
            if hasattr(g, name):
                try:
                    r = getattr(g, name)()
                except TypeError:
                    r = getattr(g, name)(True)
                return g if r is None else r
        raise RuntimeError("Dagger operation is unavailable")

    def _control(g, ctrls):
        for name in ("control", "set_control", "setControl"):
            if hasattr(g, name):
                r = getattr(g, name)(ctrls)
                return g if r is None else r
        raise RuntimeError("Control operation is unavailable")

    qvm = _init_machine()
    q = _alloc_qubits(qvm, 3)
    prog = QProg()

    _append(prog, _gate(("H",))(q[0]))

    try:
        _append(prog, _gate(("CSWAP", "Fredkin"))(q[0], q[1], q[2]))
    except Exception:
        cnot = _gate(("CNOT", "CX"))
        try:
            ccx = _gate(("Toffoli", "CCX"))
        except Exception:
            ccx = None
        _append(prog, cnot(q[2], q[1]))
        if ccx is not None:
            _append(prog, ccx(q[0], q[1], q[2]))
        else:
            _append(prog, _control(cnot(q[1], q[2]), [q[0]]))
        _append(prog, cnot(q[2], q[1]))

    _append(prog, _gate(("H",))(q[1]))

    try:
        _append(prog, _control(_dagger(_gate(("S",))(q[0])), [q[1]]))
    except Exception:
        rz = _gate(("RZ",))
        cnot = _gate(("CNOT", "CX"))
        lam = -math.pi / 2
        _append(prog, rz(q[1], lam / 2))
        _append(prog, rz(q[0], lam / 2))
        _append(prog, cnot(q[1], q[0]))
        _append(prog, rz(q[0], -lam / 2))
        _append(prog, cnot(q[1], q[0]))

    return prog
