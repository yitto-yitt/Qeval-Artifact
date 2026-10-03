# EVAL_META: task_id=67, framework=qpanda, class=1
from math import pi
import pyqpanda3.core as pq


def chsh_circuit(alice, bob):
    def _append(container, node):
        try:
            res = container << node
            return container if res is None else res
        except Exception:
            for name in ("insert", "append", "add"):
                if hasattr(container, name):
                    res = getattr(container, name)(node)
                    return container if res is None else res
            raise

    def _gate(names, *args):
        if isinstance(names, str):
            names = (names,)
        last_exc = None
        for name in names:
            fn = getattr(pq, name, None)
            if fn is None:
                continue
            try:
                return fn(*args)
            except Exception as exc:
                last_exc = exc
        if last_exc is not None:
            raise last_exc
        raise AttributeError(names[0])

    def _ry(qubit, angle):
        last_exc = None
        for args in ((qubit, angle), (angle, qubit)):
            try:
                return _gate(("RY", "Ry", "ry"), *args)
            except Exception as exc:
                last_exc = exc
        raise last_exc

    def _measure(qubit, cbit):
        last_exc = None
        for names in (("Measure", "MEASURE", "measure"),):
            for args in ((qubit, cbit),):
                try:
                    return _gate(names, *args)
                except Exception as exc:
                    last_exc = exc
        raise last_exc

    def _make_prog():
        for cls_name in ("QProg", "QCircuit"):
            cls = getattr(pq, cls_name, None)
            if cls is None:
                continue
            for args in ((), (2,), (2, 2)):
                try:
                    return cls(*args)
                except Exception:
                    pass
        raise AttributeError("QProg")

    def _build(q, c):
        prog = _make_prog()
        prog = _append(prog, _gate(("H", "h"), q[0]))
        prog = _append(prog, _gate(("CNOT", "CX", "cnot", "cx"), q[0], q[1]))
        prog = _append(prog, _ry(q[0], 0 if alice == 0 else -pi / 2))
        prog = _append(prog, _measure(q[0], c[0]))
        prog = _append(prog, _ry(q[1], -pi / 4 if bob == 0 else pi / 4))
        prog = _append(prog, _measure(q[1], c[1]))
        return prog

    try:
        return _build([0, 1], [0, 1])
    except Exception:
        machine = pq.CPUQVM()
        for init_name in ("init_qvm", "initQVM", "init"):
            if hasattr(machine, init_name):
                try:
                    getattr(machine, init_name)()
                    break
                except Exception:
                    pass

        def _alloc_many(kind, n):
            if kind == "q":
                names = ("qAlloc_many", "qalloc_many", "qAllocMany", "allocate_qubits", "alloc_qubits")
                singles = ("qAlloc", "qalloc", "allocate_qubit", "alloc_qubit")
            else:
                names = ("cAlloc_many", "calloc_many", "cAllocMany", "allocate_cbits", "alloc_cbits")
                singles = ("cAlloc", "calloc", "allocate_cbit", "alloc_cbit")
            for name in names:
                if hasattr(machine, name):
                    try:
                        return list(getattr(machine, name)(n))
                    except Exception:
                        pass
            out = []
            for _ in range(n):
                for name in singles:
                    if hasattr(machine, name):
                        try:
                            out.append(getattr(machine, name)())
                            break
                        except Exception:
                            pass
                else:
                    raise AttributeError(kind + " allocation")
            return out

        q = _alloc_many("q", 2)
        c = _alloc_many("c", 2)
        prog = _build(q, c)
        if not hasattr(chsh_circuit, "_keepalive"):
            chsh_circuit._keepalive = []
        chsh_circuit._keepalive.append(machine)
        return prog
