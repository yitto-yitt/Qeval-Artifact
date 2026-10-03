# EVAL_META: task_id=56, framework=qpanda, class=1
from pyqpanda3.core import *

def not_gate(a):
    def _new_machine():
        m = CPUQVM()
        for name in ("init_qvm", "initQVM", "init"):
            if hasattr(m, name):
                try:
                    getattr(m, name)()
                    break
                except TypeError:
                    pass
        return m

    def _alloc_qubits(m, n):
        for name in ("qAlloc_many", "qalloc_many", "allocate_qubits", "qAllocMany"):
            if hasattr(m, name):
                return getattr(m, name)(n)
        if "qAlloc_many" in globals():
            return qAlloc_many(n)
        return [m.qAlloc() for _ in range(n)]

    def _alloc_cbits(m, n):
        for name in ("cAlloc_many", "calloc_many", "allocate_cbits", "cAllocMany"):
            if hasattr(m, name):
                return getattr(m, name)(n)
        if "cAlloc_many" in globals():
            return cAlloc_many(n)
        return [m.cAlloc() for _ in range(n)]

    def _append(prog, op):
        if hasattr(prog, "insert"):
            prog.insert(op)
        else:
            prog << op

    def _measure_op(q, c):
        if "Measure" in globals():
            return Measure(q, c)
        return measure(q, c)

    def _run_counts(m, prog, cbits, shots):
        result = None
        for name in ("run_with_configuration", "runWithConfiguration", "run_with_config"):
            if hasattr(m, name):
                result = getattr(m, name)(prog, cbits, shots)
                break
        if result is None:
            result = run_with_configuration(prog, cbits, shots)

        if hasattr(result, "get_counts"):
            result = result.get_counts()
        elif hasattr(result, "counts"):
            result = result.counts

        return dict(result)

    def _bits_from_key(key):
        s = "".join(ch for ch in str(key) if ch in "01")
        if len(s) < 8:
            s = s.zfill(8)
        elif len(s) > 8:
            s = s[-8:]
        return s

    def _cbit_order_is_forward():
        m = _new_machine()
        qs = _alloc_qubits(m, 2)
        cs = _alloc_cbits(m, 2)
        p = QProg()
        _append(p, X(qs[0]))
        _append(p, _measure_op(qs[0], cs[0]))
        _append(p, _measure_op(qs[1], cs[1]))
        counts = _run_counts(m, p, cs, 32)
        key = max(counts, key=counts.get)
        s = "".join(ch for ch in str(key) if ch in "01")
        return len(s) >= 2 and s[0] == "1"

    forward_order = _cbit_order_is_forward()

    m = _new_machine()
    qs = _alloc_qubits(m, 8)
    cs = _alloc_cbits(m, 8)
    prog = QProg()

    a_bits = format(a, "08b")
    for i in range(8):
        if a_bits[7 - i] == "0":
            _append(prog, X(qs[i]))

    if forward_order:
        for i in range(8):
            _append(prog, _measure_op(qs[7 - i], cs[i]))
    else:
        for i in range(8):
            _append(prog, _measure_op(qs[i], cs[i]))

    counts = _run_counts(m, prog, cs, 1024)
    total = sum(counts.values())
    return {_bits_from_key(key): value / total for key, value in counts.items()}
