# EVAL_META: task_id=64, framework=qpanda, class=1
import pyqpanda3.core as pq


def simons_algorithm(s):
    n = len(s)
    s = s[::-1]

    machine = pq.CPUQVM()
    for _init_name in ("init_qvm", "init", "initQVM"):
        _init = getattr(machine, _init_name, None)
        if _init is not None:
            try:
                _init()
            except TypeError:
                pass
            break

    def _alloc(obj, names, count):
        for name in names:
            fn = getattr(obj, name, None)
            if fn is not None:
                return list(fn(count))
        for name in names:
            fn = getattr(pq, name, None)
            if fn is not None:
                return list(fn(count))
        raise AttributeError("No suitable allocator found")

    q_reg1 = _alloc(machine, ("qAlloc_many", "qalloc_many", "qAllocMany"), n)
    q_reg2 = _alloc(machine, ("qAlloc_many", "qalloc_many", "qAllocMany"), n)
    c_reg = _alloc(machine, ("cAlloc_many", "calloc_many", "cAllocMany"), n)

    prog = pq.QProg()

    def _append(op):
        nonlocal prog
        try:
            ret = prog << op
            if ret is not None:
                prog = ret
            return
        except Exception:
            pass
        for name in ("insert", "append", "push_back"):
            fn = getattr(prog, name, None)
            if fn is not None:
                ret = fn(op)
                if ret is not None:
                    prog = ret
                return
        raise AttributeError("No suitable program append method found")

    cnot = getattr(pq, "CNOT", None) or getattr(pq, "CX", None)
    measure = getattr(pq, "Measure", None) or getattr(pq, "measure", None)

    for q in q_reg1:
        _append(pq.H(q))

    for j in range(n):
        _append(cnot(q_reg1[j], q_reg2[j]))

    if "1" in s:
        i = s.find("1")
        for j in range(n):
            if s[j] == "1":
                _append(cnot(q_reg1[i], q_reg2[j]))
        for q in q_reg1:
            _append(pq.H(q))

    for j in range(n):
        _append(measure(q_reg1[j], c_reg[j]))

    if not hasattr(simons_algorithm, "_resources"):
        simons_algorithm._resources = []
    simons_algorithm._resources.append((machine, q_reg1, q_reg2, c_reg))

    return prog
