# EVAL_META: task_id=3, framework=qpanda, class=2
import pyqpanda3.core as pq
from pyqpanda3.core import *


def create_ghz(drawing=False):
    def _make_machine():
        cls = getattr(pq, "CPUQVM", None) or getattr(pq, "CpuQVM", None)
        if cls is None:
            raise AttributeError("CPUQVM is not available in pyqpanda3.core")
        m = cls()
        for name in ("init_qvm", "initQVM", "init"):
            fn = getattr(m, name, None)
            if fn is not None:
                try:
                    fn()
                except Exception:
                    pass
                break
        return m

    def _alloc(m, names, n):
        last_error = None
        for name in names:
            fn = getattr(m, name, None)
            if fn is not None:
                try:
                    return fn(n)
                except TypeError as exc:
                    last_error = exc
        if last_error is not None:
            raise last_error
        raise AttributeError("required allocation method is not available")

    machine = _make_machine()
    qubits = _alloc(machine, ("qAlloc_many", "qalloc_many", "qAllocMany", "qallocMany"), 3)
    cbits = _alloc(machine, ("cAlloc_many", "calloc_many", "cAllocMany", "callocMany"), 3)

    prog = pq.QProg()

    def _append(op):
        nonlocal prog
        try:
            prog = prog << op
        except TypeError:
            if hasattr(prog, "insert"):
                prog.insert(op)
            else:
                raise

    h_gate = getattr(pq, "H")
    cnot_gate = getattr(pq, "CNOT", None) or getattr(pq, "CX", None)
    if cnot_gate is None:
        raise AttributeError("CNOT/CX is not available in pyqpanda3.core")

    _append(h_gate(qubits[0]))
    _append(cnot_gate(qubits[0], qubits[1]))
    _append(cnot_gate(qubits[0], qubits[2]))

    measured = False
    for name in ("measure_all", "MeasureAll", "measureAll"):
        fn = getattr(pq, name, None)
        if fn is not None:
            try:
                meas_ops = fn(qubits, cbits)
                if meas_ops is not None:
                    _append(meas_ops)
                measured = True
                break
            except TypeError:
                pass

    if not measured:
        measure_gate = getattr(pq, "Measure", None) or getattr(pq, "measure", None)
        if measure_gate is None:
            raise AttributeError("Measure is not available in pyqpanda3.core")
        for i in range(3):
            _append(measure_gate(qubits[i], cbits[i]))

    try:
        create_ghz._machines.append(machine)
    except AttributeError:
        create_ghz._machines = [machine]

    if drawing:
        drawing_obj = None
        for name in ("draw_qprog", "draw_qprog_text", "to_originir"):
            fn = getattr(pq, name, None)
            if fn is not None:
                try:
                    drawing_obj = fn(prog)
                    break
                except TypeError:
                    try:
                        drawing_obj = fn(prog, machine)
                        break
                    except TypeError:
                        pass
        if drawing_obj is None:
            drawing_obj = str(prog)
        return prog, drawing_obj

    return prog
