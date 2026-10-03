# EVAL_META: task_id=11, framework=qpanda, class=2
from pyqpanda3.core import *
import math

def get_statevector(circuit):
    def _call(obj, names, *args):
        for name in names:
            if hasattr(obj, name):
                attr = getattr(obj, name)
                try:
                    return attr(*args) if callable(attr) else attr
                except Exception:
                    pass
        return None

    def _as_prog(obj):
        prog_cls = globals().get("QProg")
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

    def _qindex(q):
        for name in ("get_phy_addr", "getPhysicalQubitPtr", "get_phy_addr_", "get_addr", "addr", "index"):
            if hasattr(q, name):
                attr = getattr(q, name)
                try:
                    v = attr() if callable(attr) else attr
                    return int(v)
                except Exception:
                    pass
        try:
            return int(q)
        except Exception:
            return None

    def _qubit_count(obj):
        for name in (
            "get_qubit_num", "getQubitNum", "get_qubits_num", "get_qubits_count",
            "qubit_num", "num_qubits", "qubits_num", "qubit_count"
        ):
            if hasattr(obj, name):
                attr = getattr(obj, name)
                try:
                    v = attr() if callable(attr) else attr
                    if v is not None:
                        return int(v)
                except Exception:
                    pass

        qubits = None
        for fname in ("get_all_used_qubits", "get_used_qubits"):
            f = globals().get(fname)
            if f is not None:
                try:
                    qubits = f(obj)
                    break
                except Exception:
                    pass

        if qubits is None:
            for name in ("get_used_qubits", "get_all_used_qubits", "qubits", "qbits"):
                if hasattr(obj, name):
                    attr = getattr(obj, name)
                    try:
                        qubits = attr() if callable(attr) else attr
                        break
                    except Exception:
                        pass

        if qubits is not None:
            try:
                idxs = [_qindex(q) for q in qubits]
                idxs = [i for i in idxs if i is not None and i >= 0]
                if idxs:
                    return max(idxs) + 1
                return 0
            except Exception:
                pass

        return None

    prog = _as_prog(circuit)
    n = _qubit_count(prog)

    qvm_cls = globals().get("CPUQVM")
    if qvm_cls is not None:
        try:
            qvm = qvm_cls()
            _call(qvm, ("init_qvm", "init", "initQVM"))

            if n is not None and n > 0:
                _call(qvm, ("qAlloc_many", "qalloc_many", "qAllocMany", "allocate_qubits"), n)

            ran = False
            for run_name in ("directly_run", "directlyRun", "run", "run_qprog", "runQProg"):
                if hasattr(qvm, run_name):
                    try:
                        getattr(qvm, run_name)(prog)
                        ran = True
                        break
                    except Exception:
                        pass

            if ran:
                state = _call(qvm, ("get_qstate", "getQState", "get_quantum_state", "get_state", "get_statevector"))
                if state is not None:
                    try:
                        if n is None or len(state) == (1 << n):
                            return state
                    except Exception:
                        return state
                    return state
        except Exception:
            pass

    for cls_name in ("StateVectorSimulator", "StatevectorSimulator", "state_vector_simulator"):
        sim_cls = globals().get(cls_name)
        if sim_cls is not None:
            try:
                sim = sim_cls()
                _call(sim, ("init_qvm", "init", "initQVM"))
                for run_name in ("run", "directly_run", "directlyRun", "run_qprog", "runQProg"):
                    if hasattr(sim, run_name):
                        try:
                            getattr(sim, run_name)(prog)
                            state = _call(sim, ("get_qstate", "getQState", "get_statevector", "get_state"))
                            if state is not None:
                                return state
                        except Exception:
                            pass
            except Exception:
                pass

    mat = None
    for target in (circuit, prog):
        mat = _call(target, ("get_matrix", "matrix"))
        if mat is not None:
            break

    if mat is None:
        f = globals().get("get_matrix")
        if f is not None:
            try:
                mat = f(prog)
            except Exception:
                try:
                    mat = f(circuit)
                except Exception:
                    mat = None

    if mat is not None:
        try:
            shape = getattr(mat, "shape", None)
            if shape is not None and len(shape) == 2:
                return [mat[i, 0] for i in range(int(shape[0]))]
        except Exception:
            pass

        try:
            rows = list(mat)
            if rows and hasattr(rows[0], "__iter__"):
                return [row[0] for row in rows]
            dim = math.isqrt(len(rows))
            if dim * dim == len(rows):
                return [rows[i * dim] for i in range(dim)]
        except Exception:
            pass

    raise RuntimeError("Unable to compute statevector with pyQPanda3")
