# EVAL_META: task_id=92, framework=qpanda, class=1
import pyqpanda3.core as pq
from pyqpanda3.core import *

def calculate_stabilizer_state_info():
    def _append(prog, gate):
        try:
            ret = prog << gate
            return prog if ret is None else ret
        except Exception:
            pass
        try:
            ret = prog.insert(gate)
            return prog if ret is None else ret
        except Exception:
            pass
        try:
            ret = prog.append(gate)
            return prog if ret is None else ret
        except Exception as exc:
            raise exc

    def _gate(name_options, *args):
        last = None
        for name in name_options:
            if hasattr(pq, name):
                try:
                    return getattr(pq, name)(*args)
                except Exception as exc:
                    last = exc
        if last is not None:
            raise last
        raise AttributeError(str(name_options))

    def _build_prog(qubits):
        last = None
        for ctor_args in ((), (2,)):
            try:
                prog = pq.QProg(*ctor_args)
                prog = _append(prog, _gate(("H",), qubits[0]))
                prog = _append(prog, _gate(("CNOT", "CX"), qubits[0], qubits[1]))
                return prog
            except Exception as exc:
                last = exc
        raise last

    def _clean_result(res):
        if res is None:
            return None
        out = {}
        if isinstance(res, dict):
            for k, v in res.items():
                try:
                    p = float(v)
                except Exception:
                    continue
                if abs(p) <= 1e-12:
                    continue
                if isinstance(k, str):
                    key = "".join(ch for ch in k if ch in "01")
                    if len(key) < 2:
                        try:
                            key = format(int(k), "02b")
                        except Exception:
                            key = k
                    elif len(key) > 2:
                        key = key[-2:]
                else:
                    key = format(int(k), "02b")
                out[key] = p
        elif isinstance(res, (list, tuple)):
            for i, v in enumerate(res):
                try:
                    p = float(abs(v) ** 2 if isinstance(v, complex) else v)
                except Exception:
                    continue
                if abs(p) > 1e-12:
                    out[format(i, "02b")] = p
        if not out:
            return None
        for k in list(out.keys()):
            if abs(out[k] - 0.5) < 1e-10:
                out[k] = 0.5
            elif abs(out[k] - 1.0) < 1e-10:
                out[k] = 1.0
            elif abs(out[k]) < 1e-10:
                del out[k]
        return dict(sorted(out.items()))

    def _state_to_probs(state):
        try:
            return _clean_result([abs(a) ** 2 for a in state[:4]])
        except Exception:
            return None

    def _init_machine(qvm):
        for name in ("init_qvm", "initQVM", "init"):
            if hasattr(qvm, name):
                try:
                    getattr(qvm, name)()
                    return
                except Exception:
                    pass

    def _alloc_qubits(qvm):
        for name in ("qAlloc_many", "qalloc_many", "qAllocMany", "allocate_qubits"):
            if hasattr(qvm, name):
                try:
                    return getattr(qvm, name)(2)
                except Exception:
                    pass
        return [0, 1]

    def _run_exact(qvm, prog, qubits):
        for name in ("prob_run_dict", "probRunDict"):
            if hasattr(qvm, name):
                for args in ((prog, qubits, -1), (prog, qubits), (prog, qubits, 0)):
                    try:
                        ans = _clean_result(getattr(qvm, name)(*args))
                        if ans is not None:
                            return ans
                    except Exception:
                        pass

        for name in ("prob_run_list", "probRunList"):
            if hasattr(qvm, name):
                for args in ((prog, qubits, -1), (prog, qubits), (prog, qubits, 0)):
                    try:
                        ans = _clean_result(getattr(qvm, name)(*args))
                        if ans is not None:
                            return ans
                    except Exception:
                        pass

        for run_name in ("directly_run", "directlyRun", "run", "execute", "run_qprog"):
            if hasattr(qvm, run_name):
                try:
                    getattr(qvm, run_name)(prog)
                    break
                except Exception:
                    pass

        for name in ("get_prob_dict", "getProbDict", "get_probabilities", "probabilities"):
            if hasattr(qvm, name):
                for args in ((qubits,), (qubits, -1), ()):
                    try:
                        ans = _clean_result(getattr(qvm, name)(*args))
                        if ans is not None:
                            return ans
                    except Exception:
                        pass

        for name in ("get_prob_list", "getProbList"):
            if hasattr(qvm, name):
                for args in ((qubits,), (qubits, -1), ()):
                    try:
                        ans = _clean_result(getattr(qvm, name)(*args))
                        if ans is not None:
                            return ans
                    except Exception:
                        pass

        for name in ("get_qstate", "getQState", "get_state", "getState"):
            if hasattr(qvm, name):
                try:
                    ans = _state_to_probs(getattr(qvm, name)())
                    if ans is not None:
                        return ans
                except Exception:
                    pass
        return None

    for machine_name in ("CPUQVM", "CPUSingleThreadQVM", "GPUQVM", "QVM"):
        if hasattr(pq, machine_name):
            try:
                qvm = getattr(pq, machine_name)()
                _init_machine(qvm)
                qubits = _alloc_qubits(qvm)
                prog = _build_prog(qubits)
                ans = _run_exact(qvm, prog, qubits)
                if ans is not None:
                    return ans
            except Exception:
                pass

    if hasattr(pq, "init"):
        try:
            if hasattr(pq, "QMachineType") and hasattr(pq.QMachineType, "CPU"):
                pq.init(pq.QMachineType.CPU)
            else:
                pq.init()
            qubits = pq.qAlloc_many(2) if hasattr(pq, "qAlloc_many") else [0, 1]
            prog = _build_prog(qubits)
            for name in ("prob_run_dict", "probRunDict"):
                if hasattr(pq, name):
                    for args in ((prog, qubits, -1), (prog, qubits), (prog, qubits, 0)):
                        try:
                            ans = _clean_result(getattr(pq, name)(*args))
                            if ans is not None:
                                return ans
                        except Exception:
                            pass
            for name in ("directly_run", "directlyRun"):
                if hasattr(pq, name):
                    try:
                        getattr(pq, name)(prog)
                        break
                    except Exception:
                        pass
            for name in ("get_qstate", "getQState"):
                if hasattr(pq, name):
                    ans = _state_to_probs(getattr(pq, name)())
                    if ans is not None:
                        return ans
        finally:
            if hasattr(pq, "finalize"):
                try:
                    pq.finalize()
                except Exception:
                    pass

    qubits = [0, 1]
    prog = _build_prog(qubits)
    for cls_name in ("StateVector", "Statevector", "QuantumState"):
        if hasattr(pq, cls_name):
            try:
                obj = getattr(pq, cls_name)(prog)
                for name in ("probabilities_dict", "probabilities", "get_probs", "get_probabilities", "data"):
                    if hasattr(obj, name):
                        attr = getattr(obj, name)
                        res = attr() if callable(attr) else attr
                        ans = _clean_result(res)
                        if ans is not None:
                            return ans
                ans = _clean_result(obj)
                if ans is not None:
                    return ans
            except Exception:
                pass

    raise RuntimeError("Unable to obtain probabilities from pyqpanda3")
