# EVAL_META: task_id=3, framework=qpanda, class=2
import pyqpanda3.core as pq


def create_ghz(drawing=False):
    def _new_prog():
        last_err = None
        for args in ((), (3,), (3, 3)):
            try:
                return pq.QProg(*args)
            except Exception as exc:
                last_err = exc
        raise last_err

    def _append(prog, op):
        try:
            out = prog << op
            return prog if out is None else out
        except Exception:
            try:
                prog.insert(op)
                return prog
            except Exception:
                prog.append(op)
                return prog

    def _init_machine():
        cls = getattr(pq, "CPUQVM", None)
        if cls is None:
            return None
        machine = cls()
        for name in ("init_qvm", "initQVM", "init"):
            method = getattr(machine, name, None)
            if callable(method):
                try:
                    method()
                    break
                except Exception:
                    pass
        return machine

    def _alloc(machine):
        if machine is not None:
            q = c = None
            for name in ("qAlloc_many", "qalloc_many", "qAllocMany"):
                method = getattr(machine, name, None)
                if callable(method):
                    try:
                        q = method(3)
                        break
                    except Exception:
                        pass
            for name in ("cAlloc_many", "calloc_many", "cAllocMany"):
                method = getattr(machine, name, None)
                if callable(method):
                    try:
                        c = method(3)
                        break
                    except Exception:
                        pass
            if q is not None and c is not None:
                return q, c

        q_alloc = getattr(pq, "qAlloc_many", None)
        c_alloc = getattr(pq, "cAlloc_many", None)
        if callable(q_alloc) and callable(c_alloc):
            try:
                return q_alloc(3), c_alloc(3)
            except Exception:
                pass

        return [0, 1, 2], [0, 1, 2]

    def _build(use_machine):
        machine = _init_machine() if use_machine else None
        q, c = _alloc(machine)
        prog = _new_prog()

        h_gate = getattr(pq, "H")
        cx_gate = getattr(pq, "CNOT", None) or getattr(pq, "CX")

        prog = _append(prog, h_gate(q[0]))
        prog = _append(prog, cx_gate(q[0], q[1]))
        prog = _append(prog, cx_gate(q[0], q[2]))

        measure_gate = getattr(pq, "Measure", None) or getattr(pq, "measure", None)
        if callable(measure_gate):
            prog = _append(prog, measure_gate(q[0], c[0]))
            prog = _append(prog, measure_gate(q[1], c[1]))
            prog = _append(prog, measure_gate(q[2], c[2]))
        else:
            measure_all = getattr(pq, "measure_all")
            prog = _append(prog, measure_all(q, c))

        if not hasattr(create_ghz, "_resources"):
            create_ghz._resources = []
        create_ghz._resources.append((machine, q, c))
        return prog

    try:
        ghz = _build(True)
    except Exception:
        ghz = _build(False)

    if drawing:
        drawing_obj = None
        for name in ("draw", "to_draw"):
            method = getattr(ghz, name, None)
            if callable(method):
                try:
                    drawing_obj = method()
                    break
                except Exception:
                    pass
        if drawing_obj is None:
            for name in ("draw_qprog", "draw_qprog_text"):
                func = getattr(pq, name, None)
                if callable(func):
                    try:
                        drawing_obj = func(ghz)
                        break
                    except Exception:
                        pass
        if drawing_obj is None:
            drawing_obj = str(ghz)
        return ghz, drawing_obj

    return ghz
