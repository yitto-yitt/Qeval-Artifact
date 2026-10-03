# EVAL_META: task_id=11, framework=qpanda, class=2
import pyqpanda3.core as pq

def get_statevector(circuit):
    def _to_prog(obj):
        if obj.__class__.__name__ == "QProg":
            return obj
        prog_cls = getattr(pq, "QProg", None)
        if prog_cls is None:
            return obj
        try:
            if isinstance(obj, prog_cls):
                return obj
        except Exception:
            pass
        try:
            prog = prog_cls()
            prog << obj
            return prog
        except Exception:
            return obj

    def _as_int(value):
        try:
            if callable(value):
                value = value()
            return int(value)
        except Exception:
            return None

    def _qubit_addr(qubit):
        for name in (
            "get_phy_addr",
            "get_virt_addr",
            "getPhysicalQubitPtr",
            "getPhysicalQubit",
            "get_phy_addr_",
            "get_virt_addr_",
        ):
            attr = getattr(qubit, name, None)
            if attr is not None:
                val = _as_int(attr)
                if val is not None:
                    return val
        return _as_int(qubit)

    def _infer_qubit_count(obj, prog):
        for source in (obj, prog):
            for name in (
                "num_qubits",
                "qubit_num",
                "qbit_num",
                "n_qubits",
                "qnum",
                "get_qubit_num",
                "get_qbit_num",
                "get_qnum",
                "qubits_num",
            ):
                if hasattr(source, name):
                    n = _as_int(getattr(source, name))
                    if n is not None:
                        return n

        used = None
        for fn_name in (
            "get_all_used_qubits",
            "get_used_qubits",
            "get_all_qubits",
            "get_qprog_used_qubits",
        ):
            fn = getattr(pq, fn_name, None)
            if fn is not None:
                try:
                    used = fn(prog)
                    break
                except Exception:
                    try:
                        used = fn(obj)
                        break
                    except Exception:
                        pass

        if used is None:
            for source in (obj, prog):
                for name in ("qubits", "qbits", "get_qubits", "get_qbits"):
                    if hasattr(source, name):
                        attr = getattr(source, name)
                        try:
                            used = attr() if callable(attr) else attr
                            break
                        except Exception:
                            pass
                if used is not None:
                    break

        if used is not None:
            try:
                qubits = list(used)
            except Exception:
                qubits = []
            if not qubits:
                return 0
            addrs = [_qubit_addr(q) for q in qubits]
            addrs = [a for a in addrs if a is not None]
            if addrs:
                return max(addrs) + 1
            return len(qubits)

        return None

    def _init_qvm(qvm):
        for name in ("init_qvm", "init", "initialize"):
            method = getattr(qvm, name, None)
            if callable(method):
                try:
                    method()
                    return
                except Exception:
                    pass

    def _allocate_qubits(qvm, n):
        if n is None or n <= 0:
            return None
        for name in (
            "qAlloc_many",
            "qalloc_many",
            "qAllocMany",
            "qallocMany",
            "allocate_qubits",
            "alloc_qubits",
        ):
            method = getattr(qvm, name, None)
            if callable(method):
                try:
                    return method(n)
                except Exception:
                    pass
        for name in ("qAlloc", "qalloc", "allocate_qubit", "alloc_qubit"):
            method = getattr(qvm, name, None)
            if callable(method):
                qv = []
                for _ in range(n):
                    qv.append(method())
                return qv
        return None

    def _extract_state(obj, qv=None):
        for name in (
            "get_qstate",
            "get_qstate_vector",
            "get_statevector",
            "get_state_vector",
            "get_state",
            "statevector",
            "state_vector",
            "state",
        ):
            if hasattr(obj, name):
                attr = getattr(obj, name)
                if callable(attr):
                    try:
                        return attr()
                    except TypeError:
                        if qv is not None:
                            try:
                                return attr(qv)
                            except Exception:
                                pass
                    except Exception:
                        pass
                else:
                    return attr
        return None

    prog = _to_prog(circuit)

    qvm_cls = (
        getattr(pq, "CPUQVM", None)
        or getattr(pq, "QVM", None)
        or getattr(pq, "QuantumMachine", None)
    )
    if qvm_cls is None:
        raise RuntimeError("No pyQPanda3 statevector-capable QVM class is available")

    qvm = qvm_cls()
    _init_qvm(qvm)

    n_qubits = _infer_qubit_count(circuit, prog)
    qv = _allocate_qubits(qvm, n_qubits)

    run_result = None
    last_error = None
    for target in (prog, circuit):
        for name in ("directly_run", "run", "run_qprog", "execute"):
            method = getattr(qvm, name, None)
            if callable(method):
                try:
                    run_result = method(target)
                    last_error = None
                    break
                except Exception as exc:
                    last_error = exc
        if last_error is None:
            break

    if last_error is not None:
        raise last_error

    state = _extract_state(qvm, qv)
    if state is not None:
        return state

    if run_result is not None:
        state = _extract_state(run_result, qv)
        if state is not None:
            return state
        return run_result

    for fn_name in ("get_statevector", "get_qstate", "simulate_statevector"):
        fn = getattr(pq, fn_name, None)
        if callable(fn):
            for args in ((prog,), (circuit,), (qvm,), (qvm, prog), (prog, qv)):
                try:
                    return fn(*args)
                except Exception:
                    pass

    raise RuntimeError("Unable to retrieve statevector from pyQPanda3 QVM")
