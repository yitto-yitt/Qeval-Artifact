# EVAL_META: task_id=11, framework=qpanda, class=2
import pyqpanda3.core as pq

def get_statevector(circuit):
    qvm = pq.CPUQVM()

    for name in ("init_qvm", "init"):
        method = getattr(qvm, name, None)
        if callable(method):
            try:
                method()
                break
            except TypeError:
                pass

    prog = circuit
    try:
        p = pq.QProg()
        p << circuit
        prog = p
    except Exception:
        prog = circuit

    def _as_list(obj):
        try:
            return list(obj)
        except Exception:
            pass
        try:
            return [obj[i] for i in range(obj.size())]
        except Exception:
            return []

    def _int_value(obj):
        try:
            return int(obj)
        except Exception:
            return None

    def _qubit_addr(q):
        v = _int_value(q)
        if v is not None:
            return v
        for name in ("get_phy_addr", "getPhyAddr", "get_phyAddr"):
            method = getattr(q, name, None)
            if callable(method):
                try:
                    v = _int_value(method())
                    if v is not None:
                        return v
                except Exception:
                    pass
        method = getattr(q, "getPhysicalQubitPtr", None)
        if callable(method):
            try:
                ptr = method()
                for name in ("getQubitAddr", "get_qubit_addr", "get_addr"):
                    addr_method = getattr(ptr, name, None)
                    if callable(addr_method):
                        v = _int_value(addr_method())
                        if v is not None:
                            return v
            except Exception:
                pass
        return None

    n_qubits = 0

    for obj in (circuit, prog):
        for name in (
            "num_qubits",
            "qubit_num",
            "get_qubit_num",
            "get_qubits_num",
            "get_qubit_count",
            "qubits_num",
            "get_qbit_num",
        ):
            attr = getattr(obj, name, None)
            try:
                value = attr() if callable(attr) else attr
                value = _int_value(value)
                if value is not None:
                    n_qubits = max(n_qubits, value)
            except Exception:
                pass

    used_qubits = []
    for name in ("get_all_used_qubits", "get_used_qubits"):
        func = getattr(pq, name, None)
        if callable(func):
            try:
                used_qubits = _as_list(func(prog))
                if used_qubits:
                    break
            except Exception:
                pass

    if not used_qubits:
        for obj in (prog, circuit):
            for name in ("get_used_qubits", "get_all_used_qubits", "get_qvec", "qubits"):
                attr = getattr(obj, name, None)
                try:
                    value = attr() if callable(attr) else attr
                    used_qubits = _as_list(value)
                    if used_qubits:
                        break
                except Exception:
                    pass
            if used_qubits:
                break

    if used_qubits:
        addrs = []
        for q in used_qubits:
            a = _qubit_addr(q)
            if a is not None:
                addrs.append(a)
        if addrs:
            n_qubits = max(n_qubits, max(addrs) + 1)
        else:
            n_qubits = max(n_qubits, len(used_qubits))

    if n_qubits > 0:
        allocated = False
        for name in ("qAlloc_many", "qalloc_many", "qAllocMany", "qallocMany"):
            method = getattr(qvm, name, None)
            if callable(method):
                try:
                    method(n_qubits)
                    allocated = True
                    break
                except Exception:
                    pass
        if not allocated:
            for _ in range(n_qubits):
                for name in ("qAlloc", "qalloc", "allocate_qubit"):
                    method = getattr(qvm, name, None)
                    if callable(method):
                        try:
                            method()
                            break
                        except Exception:
                            pass

    executed = False
    for name in ("directly_run", "run"):
        method = getattr(qvm, name, None)
        if callable(method):
            for args in ((prog,), (prog, 1)):
                try:
                    method(*args)
                    executed = True
                    break
                except Exception:
                    pass
            if executed:
                break

    for name in ("get_qstate", "get_statevector", "get_qstate_vector", "get_state", "statevector"):
        method = getattr(qvm, name, None)
        if callable(method):
            try:
                return method()
            except Exception:
                pass

    raise RuntimeError("Unable to retrieve statevector from pyQPanda3 simulator")
