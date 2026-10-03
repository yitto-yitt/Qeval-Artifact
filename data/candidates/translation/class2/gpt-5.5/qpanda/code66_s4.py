# EVAL_META: task_id=66, framework=qpanda, class=2
from math import acos, sqrt
import pyqpanda3.core as pq


def w_state():
    def _init_machine(machine):
        for name in ("init_qvm", "initQVM", "init"):
            if hasattr(machine, name):
                try:
                    getattr(machine, name)()
                    return
                except Exception:
                    pass

    def _alloc_many(machine, many_names, single_names, n):
        last_error = None
        for name in many_names:
            if hasattr(machine, name):
                try:
                    return list(getattr(machine, name)(n))
                except Exception as exc:
                    last_error = exc
        for name in single_names:
            if hasattr(machine, name):
                try:
                    return [getattr(machine, name)() for _ in range(n)]
                except Exception as exc:
                    last_error = exc
        if last_error is not None:
            raise last_error
        raise AttributeError("No suitable allocation method found.")

    qvm = pq.CPUQVM()
    _init_machine(qvm)

    q = _alloc_many(
        qvm,
        ("qAlloc_many", "qalloc_many", "qAllocMany", "allocate_qubits", "alloc_qubits"),
        ("qAlloc", "qalloc", "qAllocOne", "allocate_qubit", "alloc_qubit"),
        3,
    )
    c = _alloc_many(
        qvm,
        ("cAlloc_many", "calloc_many", "cAllocMany", "allocate_cbits", "alloc_cbits"),
        ("cAlloc", "calloc", "cAllocOne", "allocate_cbit", "alloc_cbit"),
        3,
    )

    prog = pq.QProg()

    def _append(op):
        nonlocal prog
        try:
            result = prog << op
            if result is not None:
                prog = result
            return
        except Exception:
            pass
        result = prog.insert(op)
        if result is not None:
            prog = result

    theta = 2 * acos(1 / sqrt(3))

    _append(pq.RY(q[0], theta))

    if hasattr(pq, "CH"):
        ch_gate = pq.CH(q[0], q[1])
    else:
        ch_gate = pq.H(q[1])
        if hasattr(ch_gate, "control"):
            result = ch_gate.control([q[0]])
            if result is not None:
                ch_gate = result
        elif hasattr(ch_gate, "set_control"):
            result = ch_gate.set_control([q[0]])
            if result is not None:
                ch_gate = result
    _append(ch_gate)

    if hasattr(pq, "CNOT"):
        _append(pq.CNOT(q[1], q[2]))
        _append(pq.CNOT(q[0], q[1]))
    else:
        _append(pq.CX(q[1], q[2]))
        _append(pq.CX(q[0], q[1]))

    _append(pq.X(q[0]))

    measured = False
    for measure_name in ("Measure", "measure"):
        if hasattr(pq, measure_name):
            measure_func = getattr(pq, measure_name)
            for i in range(3):
                _append(measure_func(q[i], c[i]))
            measured = True
            break

    if not measured:
        for measure_all_name in ("measure_all", "MeasureAll"):
            if hasattr(pq, measure_all_name):
                _append(getattr(pq, measure_all_name)(q, c))
                measured = True
                break

    w_state._qvm = qvm
    w_state._qubits = q
    w_state._cbits = c
    return prog
