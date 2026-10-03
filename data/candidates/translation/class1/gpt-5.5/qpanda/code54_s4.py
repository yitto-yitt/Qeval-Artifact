# EVAL_META: task_id=54, framework=qpanda, class=1
import pyqpanda3.core as pq

def and_gate(a, b):
    def _get_callable(names):
        containers = [pq, getattr(pq, "gate", None), getattr(pq, "gates", None)]
        for container in containers:
            if container is None:
                continue
            for name in names:
                if hasattr(container, name):
                    return getattr(container, name)
        return None

    def _call_any(obj, names, *args):
        for name in names:
            if hasattr(obj, name):
                try:
                    return getattr(obj, name)(*args)
                except TypeError:
                    continue
        raise AttributeError(str(names))

    def _seq(obj, n):
        try:
            return [obj[i] for i in range(n)]
        except Exception:
            return list(obj)

    def _add(prog, op):
        try:
            prog << op
            return prog
        except Exception:
            try:
                prog.insert(op)
                return prog
            except Exception:
                return prog << op

    def _x_gate(q):
        fn = _get_callable(("X", "x"))
        if fn is None:
            raise RuntimeError("X gate is unavailable")
        return fn(q)

    def _ccx_gate(c0, c1, t):
        fn = _get_callable(("Toffoli", "CCX", "ccx"))
        if fn is not None:
            try:
                return fn(c0, c1, t)
            except Exception:
                pass
        g = _x_gate(t)
        for name in ("control", "set_control", "setControl"):
            if hasattr(g, name):
                r = getattr(g, name)([c0, c1])
                return g if r is None else r
        raise RuntimeError("controlled X gate is unavailable")

    def _measure_op(q, c):
        fn = _get_callable(("Measure", "measure"))
        if fn is None:
            raise RuntimeError("Measure is unavailable")
        return fn(q, c)

    def _clean_key(k):
        if isinstance(k, bytes):
            k = k.decode()
        if isinstance(k, int):
            return format(k, "03b")
        s = str(k).strip().replace(" ", "")
        if s.startswith("0b"):
            s = s[2:]
        s = "".join(ch for ch in s if ch in "01")
        if len(s) < 3:
            s = s.zfill(3)
        if len(s) > 3:
            s = s[-3:]
        return s

    def _normalize(result):
        if not isinstance(result, dict):
            try:
                vals = list(result)
                d = {}
                for i, v in enumerate(vals):
                    fv = float(v)
                    if fv > 1e-12:
                        d[format(i, "03b")] = fv
                total = sum(d.values())
                if total > 0:
                    return {k: v / total for k, v in d.items()}
            except Exception:
                return None
            return None
        d = {}
        for k, v in result.items():
            try:
                fv = float(v)
            except Exception:
                continue
            if fv > 1e-12:
                key = _clean_key(k)
                d[key] = d.get(key, 0.0) + fv
        total = sum(d.values())
        if total <= 0:
            return None
        return {k: v / total for k, v in d.items()}

    if hasattr(pq, "CPUQVM"):
        qvm = pq.CPUQVM()
        for init_name in ("init_qvm", "init", "initQVM"):
            if hasattr(qvm, init_name):
                try:
                    getattr(qvm, init_name)()
                    break
                except TypeError:
                    pass
    elif hasattr(pq, "init_quantum_machine"):
        qmt = getattr(pq, "QMachineType")
        cpu_type = getattr(qmt, "CPU", None)
        if cpu_type is None:
            cpu_type = getattr(qmt, "CPU_SINGLE_THREAD", None)
        qvm = pq.init_quantum_machine(cpu_type)
    else:
        raise RuntimeError("No QVM is available")

    try:
        qraw = _call_any(qvm, ("qAlloc_many", "qalloc_many", "qAllocMany", "qallocMany"), 9)
    except Exception:
        qalloc = None
        for name in ("qAlloc", "qalloc", "allocate_qubit", "allocateQubit"):
            if hasattr(qvm, name):
                qalloc = getattr(qvm, name)
                break
        if qalloc is None:
            raise
        qraw = [qalloc() for _ in range(9)]

    try:
        craw = _call_any(qvm, ("cAlloc_many", "calloc_many", "cAllocMany", "callocMany"), 3)
    except Exception:
        calloc = None
        for name in ("cAlloc", "calloc", "allocate_cbit", "allocateCBit"):
            if hasattr(qvm, name):
                calloc = getattr(qvm, name)
                break
        if calloc is None:
            raise
        craw = [calloc() for _ in range(3)]

    qubits = _seq(qraw, 9)
    cbits = _seq(craw, 3)

    prog = pq.QProg()
    a_bits = format(a, "03b")
    b_bits = format(b, "03b")

    for i in range(3):
        if a_bits[2 - i] == "1":
            _add(prog, _x_gate(qubits[i]))
        if b_bits[2 - i] == "1":
            _add(prog, _x_gate(qubits[3 + i]))

    for i in range(3):
        _add(prog, _ccx_gate(qubits[i], qubits[3 + i], qubits[6 + i]))

    probe = [qubits[8], qubits[7], qubits[6]]

    for name in ("prob_run_dict", "probRunDict", "prob_run_tuple_list"):
        if hasattr(qvm, name):
            fn = getattr(qvm, name)
            for args in ((prog, probe, -1), (prog, probe), (prog, probe, 8)):
                try:
                    dist = _normalize(fn(*args))
                    if dist is not None:
                        return dist
                except Exception:
                    pass

    for name in ("prob_run_list", "probRunList"):
        if hasattr(qvm, name):
            fn = getattr(qvm, name)
            for args in ((prog, probe, -1), (prog, probe), (prog, probe, 8)):
                try:
                    dist = _normalize(fn(*args))
                    if dist is not None:
                        return dist
                except Exception:
                    pass

    for i in range(3):
        _add(prog, _measure_op(qubits[8 - i], cbits[i]))

    shots = 1024
    for name in ("run_with_configuration", "runWithConfiguration", "run"):
        if hasattr(qvm, name):
            fn = getattr(qvm, name)
            for args in ((prog, cbits, shots), (prog, shots, cbits), (prog, shots)):
                try:
                    dist = _normalize(fn(*args))
                    if dist is not None:
                        return dist
                except Exception:
                    pass

    raise RuntimeError("Quantum program execution failed")
