# EVAL_META: task_id=12, framework=qpanda, class=3
import numpy as np
import pyqpanda3.core as pq


def get_unitary():
    def _new_qvm():
        cls = getattr(pq, "CPUQVM")
        last = None
        for args in ((), (2,)):
            try:
                qvm = cls(*args)
                break
            except Exception as exc:
                last = exc
        else:
            raise last

        for name in ("set_configure", "setConfigure", "set_config", "setConfig"):
            method = getattr(qvm, name, None)
            if callable(method):
                for args in ((2, 2), (2, 0), (2,)):
                    try:
                        method(*args)
                        break
                    except Exception:
                        pass
                break

        for name in ("init_qvm", "initQVM", "init", "initialize"):
            method = getattr(qvm, name, None)
            if callable(method):
                try:
                    method()
                    break
                except Exception:
                    pass
        return qvm

    def _as_qubit_list(obj, n):
        try:
            return [obj[i] for i in range(n)]
        except Exception:
            try:
                return list(obj)[:n]
            except Exception:
                return None

    def _alloc_qubits(qvm, n=2):
        for name in (
            "qAlloc_many",
            "qalloc_many",
            "qAllocMany",
            "qallocMany",
            "allocate_qubits",
            "allocateQubits",
        ):
            method = getattr(qvm, name, None)
            if callable(method):
                try:
                    qs = _as_qubit_list(method(n), n)
                    if qs is not None and len(qs) == n:
                        return qs
                except Exception:
                    pass

        for name in ("qAlloc", "qalloc", "allocate_qubit", "allocateQubit"):
            method = getattr(qvm, name, None)
            if callable(method):
                try:
                    return [method() for _ in range(n)]
                except Exception:
                    pass

        return list(range(n))

    def _gate(kind, *args):
        names = {
            "H": ("H", "h"),
            "X": ("X", "x"),
            "CNOT": ("CNOT", "cnot", "CX", "cx"),
        }[kind]
        last = None
        for name in names:
            fn = getattr(pq, name, None)
            if callable(fn):
                try:
                    return fn(*args)
                except Exception as exc:
                    last = exc
                if len(args) == 2:
                    try:
                        return fn([args[0], args[1]])
                    except Exception as exc:
                        last = exc
        raise last

    def _append(prog, gate):
        try:
            out = prog << gate
            return prog if out is None else out
        except Exception:
            pass
        for name in ("insert", "append", "push_back", "add"):
            method = getattr(prog, name, None)
            if callable(method):
                try:
                    out = method(gate)
                    return prog if out is None else out
                except Exception:
                    pass
        raise RuntimeError("Unable to append gate to QProg")

    def _make_program(prep_bits=0, bell=True, force_two_qubits=False):
        qvm = _new_qvm()
        qs = _alloc_qubits(qvm, 2)
        prog = pq.QProg()

        for i in range(2):
            if (prep_bits >> i) & 1:
                prog = _append(prog, _gate("X", qs[i]))

        if bell:
            prog = _append(prog, _gate("H", qs[0]))
            prog = _append(prog, _gate("CNOT", qs[0], qs[1]))

        if force_two_qubits:
            for i in range(2):
                prog = _append(prog, _gate("X", qs[i]))
                prog = _append(prog, _gate("X", qs[i]))

        return qvm, qs, prog

    def _state_array(obj):
        if obj is None or isinstance(obj, dict):
            return None

        for name in ("to_numpy", "numpy", "to_list", "tolist"):
            method = getattr(obj, name, None)
            if callable(method):
                try:
                    arr = _state_array(method())
                    if arr is not None:
                        return arr
                except Exception:
                    pass

        for name in (
            "get_qstate",
            "getQState",
            "get_qstate_vector",
            "get_state",
            "getState",
            "get_statevector",
            "getStateVector",
            "statevector",
            "qstate",
            "state",
        ):
            attr = getattr(obj, name, None)
            if attr is not None:
                try:
                    val = attr() if callable(attr) else attr
                    if val is not obj:
                        arr = _state_array(val)
                        if arr is not None:
                            return arr
                except Exception:
                    pass

        try:
            arr = np.asarray(obj, dtype=complex).reshape(-1)
            if arr.size >= 4:
                return arr
        except Exception:
            pass
        return None

    def _run_state(prep_bits, bell):
        qvm, qs, prog = _make_program(prep_bits, bell, False)
        result = None

        for name in (
            "directly_run",
            "directlyRun",
            "run",
            "execute",
            "run_qprog",
            "runQProg",
        ):
            method = getattr(qvm, name, None)
            if callable(method):
                for args in ((prog,), (prog, 1)):
                    try:
                        result = method(*args)
                        break
                    except Exception:
                        pass
                else:
                    continue
                break

        arr = _state_array(qvm)
        if arr is None:
            arr = _state_array(result)
        if arr is None or arr.size < 4:
            raise RuntimeError("Unable to obtain statevector")
        return arr

    def _matrix_array(obj):
        if obj is None:
            return None

        for name in ("to_numpy", "numpy", "to_matrix", "matrix", "get_matrix", "tolist", "to_list"):
            method = getattr(obj, name, None)
            if callable(method):
                try:
                    arr = _matrix_array(method())
                    if arr is not None:
                        return arr
                except Exception:
                    pass

        try:
            arr = np.asarray(obj, dtype=complex)
            if arr.ndim == 1:
                root = int(round(np.sqrt(arr.size)))
                if root * root == arr.size:
                    arr = arr.reshape(root, root)
            if arr.ndim == 2 and arr.shape[0] >= 4 and arr.shape[1] >= 4:
                return arr
        except Exception:
            pass
        return None

    def _extract_matrix(prog, qs):
        for name in ("matrix", "to_matrix", "get_matrix", "getMatrix", "unitary", "get_unitary"):
            method = getattr(prog, name, None)
            if callable(method):
                for args in ((), (2,), (qs,), ([qs[0], qs[1]],)):
                    try:
                        arr = _matrix_array(method(*args))
                        if arr is not None:
                            return arr
                    except Exception:
                        pass

        for name in (
            "get_matrix",
            "getMatrix",
            "get_unitary",
            "getUnitary",
            "getCircuitMatrix",
            "get_circuit_matrix",
            "circuit_matrix",
        ):
            fn = getattr(pq, name, None)
            if callable(fn):
                for args in ((prog,), (prog, 2), (prog, qs), (prog, [qs[0], qs[1]])):
                    try:
                        arr = _matrix_array(fn(*args))
                        if arr is not None:
                            return arr
                    except Exception:
                        pass
        raise RuntimeError("Unable to extract matrix")

    try:
        basis_to_internal = {}
        for b in range(4):
            state = _run_state(b, False)
            basis_to_internal[b] = int(np.argmax(np.abs(state)))

        u = np.zeros((4, 4), dtype=complex)
        for col in range(4):
            state = _run_state(col, True)
            for row in range(4):
                u[row, col] = state[basis_to_internal[row]]
        return u
    except Exception:
        basis_to_internal = {}
        for b in range(4):
            _, qs, prog = _make_program(b, False, True)
            prep = _extract_matrix(prog, qs)
            basis_to_internal[b] = int(np.argmax(np.abs(prep[:, 0])))

        _, qs, prog = _make_program(0, True, True)
        mat = _extract_matrix(prog, qs)

        u = np.zeros((4, 4), dtype=complex)
        for row in range(4):
            for col in range(4):
                u[row, col] = mat[basis_to_internal[row], basis_to_internal[col]]
        return u
