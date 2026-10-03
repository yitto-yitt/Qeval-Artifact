# EVAL_META: task_id=65, framework=qpanda, class=3
import math
import pyqpanda3.core as pq

def QFT(n):
    machine = pq.CPUQVM()
    for _init_name in ("init_qvm", "init"):
        _init = getattr(machine, _init_name, None)
        if callable(_init):
            try:
                _init()
                break
            except Exception:
                pass

    qubits = []
    if n > 0:
        for _alloc_name in ("qAlloc_many", "qalloc_many", "qAllocMany"):
            _alloc = getattr(machine, _alloc_name, None)
            if callable(_alloc):
                try:
                    qubits = list(_alloc(n))
                    break
                except Exception:
                    pass
        if not qubits:
            _alloc_one = getattr(machine, "qAlloc", None)
            if callable(_alloc_one):
                qubits = [_alloc_one() for _ in range(n)]

    prog = pq.QProg()

    def _append(op):
        nonlocal prog
        try:
            res = prog << op
            if res is not None:
                prog = res
        except Exception:
            res = prog.insert(op)
            if res is not None:
                prog = res

    def _try_append_gate(names, variants):
        for name in names:
            gate_fn = getattr(pq, name, None)
            if gate_fn is None:
                continue
            for args in variants:
                try:
                    _append(gate_fn(*args))
                    return True
                except Exception:
                    pass
        return False

    def _h(i):
        if not _try_append_gate(("H",), ((qubits[i],),)):
            raise RuntimeError("H gate is not available in pyqpanda3.core")

    def _cnot(c, t):
        if not _try_append_gate(("CNOT", "CX"), ((qubits[c], qubits[t]),)):
            raise RuntimeError("CNOT/CX gate is not available in pyqpanda3.core")

    def _swap(a, b):
        if not _try_append_gate(("SWAP", "Swap"), ((qubits[a], qubits[b]),)):
            _cnot(a, b)
            _cnot(b, a)
            _cnot(a, b)

    def _phase_gate_exact(i, theta):
        for name in ("U1", "P", "PHASE", "Phase"):
            gate_fn = getattr(pq, name, None)
            if gate_fn is None:
                continue
            for args in ((qubits[i], theta), (theta, qubits[i])):
                try:
                    return gate_fn(*args)
                except Exception:
                    pass
        return None

    def _append_phase(i, theta):
        if _try_append_gate(("U1", "P", "PHASE", "Phase"), ((qubits[i], theta), (theta, qubits[i]))):
            return
        if _try_append_gate(("RZ", "Rz"), ((qubits[i], theta), (theta, qubits[i]))):
            return
        raise RuntimeError("No phase/RZ gate is available in pyqpanda3.core")

    def _controlled_phase(c, t, theta):
        if _try_append_gate(
            ("CP", "CR", "CU1"),
            ((qubits[c], qubits[t], theta), (theta, qubits[c], qubits[t])),
        ):
            return

        gate = _phase_gate_exact(t, theta)
        if gate is not None:
            for method_name in ("control", "set_control"):
                method = getattr(gate, method_name, None)
                if callable(method):
                    for ctrl_arg in ([qubits[c]], (qubits[c],), qubits[c]):
                        try:
                            controlled_gate = method(ctrl_arg)
                            _append(controlled_gate if controlled_gate is not None else gate)
                            return
                        except Exception:
                            pass

        _append_phase(c, theta / 2.0)
        _cnot(c, t)
        _append_phase(t, -theta / 2.0)
        _cnot(c, t)
        _append_phase(t, theta / 2.0)

    def _qft_rotations(size):
        if size == 0:
            return
        size -= 1
        _h(size)
        for qubit in range(size):
            _controlled_phase(qubit, size, math.pi / (2 ** (size - qubit)))
        _qft_rotations(size)

    _qft_rotations(n)
    for qubit in range(n // 2):
        _swap(qubit, n - qubit - 1)

    if not hasattr(QFT, "_contexts"):
        QFT._contexts = []
    QFT._contexts.append((machine, qubits))
    return prog
