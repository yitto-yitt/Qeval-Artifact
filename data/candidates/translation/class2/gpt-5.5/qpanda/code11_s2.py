# EVAL_META: task_id=11, framework=qpanda, class=2
import pyqpanda3.core as pq

def get_statevector(circuit):
    def _call(obj, name, *args):
        fn = getattr(obj, name, None)
        if callable(fn):
            try:
                return True, fn(*args)
            except Exception:
                return False, None
        return False, None

    def _make_prog(obj):
        QProg = getattr(pq, "QProg", None)
        if QProg is None:
            return obj
        try:
            if isinstance(obj, QProg):
                return obj
        except Exception:
            pass
        try:
            prog = QProg()
            prog << obj
            return prog
        except Exception:
            return obj

    def _addr(q):
        for name in ("get_phy_addr", "get_addr", "get_qaddr", "addr", "physical_addr"):
            v = getattr(q, name, None)
            try:
                v = v() if callable(v) else v
                if v is not None:
                    return int(v)
            except Exception:
                pass
        try:
            return int(q)
        except Exception:
            return None

    def _used_qubits(obj):
        for name in ("get_all_used_qubits", "get_used_qubits", "get_qprog_used_qubits"):
            fn = getattr(pq, name, None)
            if callable(fn):
                try:
                    qs = fn(obj)
                    if qs is not None:
                        return list(qs)
                except Exception:
                    pass
        for name in ("get_all_used_qubits", "get_used_qubits", "get_qubits", "qubits"):
            v = getattr(obj, name, None)
            try:
                qs = v() if callable(v) else v
                if qs is not None:
                    return list(qs)
            except Exception:
                pass
        return None

    def _num_qubits(obj):
        for name in ("num_qubits", "qubit_num", "qubits_num", "n_qubits"):
            v = getattr(obj, name, None)
            try:
                v = v() if callable(v) else v
                if v is not None:
                    return int(v)
            except Exception:
                pass
        for name in ("get_qubit_num", "get_qubits_num", "qubit_count"):
            ok, v = _call(obj, name)
            if ok and v is not None:
                try:
                    return int(v)
                except Exception:
                    pass
        qs = _used_qubits(obj)
        if qs is not None:
            addrs = [_addr(q) for q in qs]
            addrs = [a for a in addrs if a is not None and a >= 0]
            if addrs:
                return max(addrs) + 1
            return len(qs)
        return 0

    def _init_qvm(qvm):
        for name in ("init_qvm", "init", "initialize"):
            ok, _ = _call(qvm, name)
            if ok:
                return

    def _alloc(qvm, n):
        if n <= 0:
            return []
        for name in ("qalloc_many", "qAlloc_many", "q_alloc_many", "qAllocMany"):
            ok, qs = _call(qvm, name, n)
            if ok:
                try:
                    return list(qs)
                except Exception:
                    return qs
        qs = []
        for _ in range(n):
            for name in ("qalloc", "qAlloc", "q_alloc"):
                ok, q = _call(qvm, name)
                if ok:
                    qs.append(q)
                    break
        return qs

    def _state_from_qvm(qvm, prog, original, allocated):
        run_targets = []
        for x in (prog, original):
            if all(id(x) != id(y) for y in run_targets):
                run_targets.append(x)
        ran = False
        run_result = None
        for target in run_targets:
            for name in ("directly_run", "directlyRun", "run", "run_qprog"):
                ok, run_result = _call(qvm, name, target)
                if ok:
                    ran = True
                    break
            if ran:
                break
        if not ran:
            return None
        for name in ("get_qstate", "get_qstate_vector", "get_statevector", "get_state_vector", "get_quantum_state"):
            for args in ((), (allocated,), (prog,), (original,)):
                ok, state = _call(qvm, name, *args)
                if ok and state is not None:
                    return state
        if run_result is not None:
            return run_result
        return None

    prog = _make_prog(circuit)

    for name in ("get_statevector", "statevector", "simulate_statevector", "statevector_simulate"):
        fn = getattr(pq, name, None)
        if callable(fn):
            for args in ((prog,), (circuit,)):
                try:
                    state = fn(*args)
                    if state is not None:
                        return state
                except Exception:
                    pass

    for name in ("statevector", "get_statevector", "to_statevector"):
        ok, state = _call(circuit, name)
        if ok and state is not None:
            return state

    n = max(_num_qubits(circuit), _num_qubits(prog))

    for cls_name in ("CPUQVM", "CPUSingleThreadQVM", "GPUQVM"):
        cls = getattr(pq, cls_name, None)
        if cls is None:
            continue
        for do_alloc in (True, False):
            try:
                qvm = cls()
                _init_qvm(qvm)
                allocated = _alloc(qvm, n) if do_alloc else []
                state = _state_from_qvm(qvm, prog, circuit, allocated)
                if state is not None:
                    return state
            except Exception:
                pass

    try:
        allocated = []
        if hasattr(pq, "qalloc_many") and n > 0:
            allocated = list(pq.qalloc_many(n))
        elif hasattr(pq, "qAlloc_many") and n > 0:
            allocated = list(pq.qAlloc_many(n))
        for name in ("directly_run", "directlyRun", "run"):
            fn = getattr(pq, name, None)
            if callable(fn):
                try:
                    fn(prog)
                    break
                except Exception:
                    pass
        for name in ("get_qstate", "get_statevector", "get_state_vector"):
            fn = getattr(pq, name, None)
            if callable(fn):
                for args in ((), (allocated,), (prog,)):
                    try:
                        state = fn(*args)
                        if state is not None:
                            return state
                    except Exception:
                        pass
    except Exception:
        pass

    raise RuntimeError("Unable to obtain statevector with pyqpanda3.core")
