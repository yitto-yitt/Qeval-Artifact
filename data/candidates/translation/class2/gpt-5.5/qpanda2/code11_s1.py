# EVAL_META: task_id=11, framework=qpanda2, class=2
import re
import pyqpanda as pq

def get_statevector(circuit):
    def _addr(q):
        for name in ("get_phy_addr", "get_addr"):
            try:
                value = getattr(q, name)()
                if isinstance(value, int):
                    return value
            except Exception:
                pass
        try:
            return int(q)
        except Exception:
            pass
        nums = re.findall(r"\d+", str(q))
        return int(nums[-1]) if nums else None

    def _as_int(value):
        try:
            if isinstance(value, bool):
                return None
            return int(value)
        except Exception:
            return None

    def _update_from_qubits(qs, current):
        if qs is None:
            return current
        if isinstance(qs, int):
            return max(current, qs)
        try:
            for q in qs:
                a = _addr(q)
                if a is not None and a >= 0:
                    current = max(current, a + 1)
        except Exception:
            pass
        return current

    try:
        if isinstance(circuit, pq.QProg):
            prog = circuit
        else:
            prog = pq.QProg()
            prog << circuit
    except Exception:
        prog = pq.QProg()
        prog << circuit

    n_qubits = 0

    for obj in (circuit, prog):
        for name in ("num_qubits", "n_qubits", "qubit_num", "qubits_num"):
            try:
                attr = getattr(obj, name)
                value = attr() if callable(attr) else attr
                value = _as_int(value)
                if value is not None and value >= 0:
                    n_qubits = max(n_qubits, value)
            except Exception:
                pass

        for name in ("get_qubit_num", "get_qubits_num"):
            try:
                value = _as_int(getattr(obj, name)())
                if value is not None and value >= 0:
                    n_qubits = max(n_qubits, value)
            except Exception:
                pass

        for name in ("get_max_qubit_addr", "get_max_qubit_id"):
            try:
                value = _as_int(getattr(obj, name)())
                if value is not None and value >= 0:
                    n_qubits = max(n_qubits, value + 1)
            except Exception:
                pass

        for name in ("get_used_qubits", "get_qvec"):
            try:
                n_qubits = _update_from_qubits(getattr(obj, name)(), n_qubits)
            except Exception:
                pass

    for name in ("get_all_used_qubits",):
        func = getattr(pq, name, None)
        if func is not None:
            try:
                n_qubits = _update_from_qubits(func(prog), n_qubits)
            except Exception:
                pass

    for name in ("get_max_qubit_addr", "get_qprog_max_qubit_addr"):
        func = getattr(pq, name, None)
        if func is not None:
            try:
                value = _as_int(func(prog))
                if value is not None and value >= 0:
                    n_qubits = max(n_qubits, value + 1)
            except Exception:
                pass

    qvm = pq.CPUQVM()
    qvm.init_qvm()
    try:
        if n_qubits > 0:
            qvm.qAlloc_many(int(n_qubits))
        qvm.directly_run(prog)
        state = qvm.get_qstate()
        try:
            if len(state) == 0 and n_qubits == 0:
                state = [1.0 + 0.0j]
        except Exception:
            pass
    finally:
        qvm.finalize()

    return state
