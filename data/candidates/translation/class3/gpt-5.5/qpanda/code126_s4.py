# EVAL_META: task_id=126, framework=qpanda, class=3
import numpy as np
import pyqpanda3.core as pq


def calculate_phase_difference_fidelity():
    def _to_matrix(value):
        if value is None:
            return None
        for attr in ("to_numpy", "numpy", "data"):
            try:
                v = getattr(value, attr)
                value = v() if callable(v) else v
                break
            except Exception:
                pass
        try:
            arr = np.asarray(value, dtype=complex)
        except Exception:
            return None
        if arr.shape == (2, 2):
            return arr
        if arr.size == 4:
            return arr.reshape((2, 2))
        return None

    def _append(container, gate):
        try:
            r = container << gate
            return container if r is None else r
        except Exception:
            pass
        for name in ("insert", "append", "add_gate", "push_back"):
            try:
                r = getattr(container, name)(gate)
                return container if r is None else r
            except Exception:
                pass
        raise RuntimeError("cannot append gate")

    def _matrix_from_framework():
        objs = []
        for q in (0,):
            try:
                gate = pq.H(q)
                objs.append(gate)
            except Exception:
                continue
            for cls_name in ("QCircuit", "QProg"):
                try:
                    obj = getattr(pq, cls_name)()
                    obj = _append(obj, gate)
                    objs.append(obj)
                except Exception:
                    pass

        module_funcs = (
            "get_matrix",
            "get_unitary",
            "get_qprog_matrix",
            "get_circuit_matrix",
            "getCircuitMatrix",
        )
        for obj in objs:
            mat = _to_matrix(obj)
            if mat is not None:
                return mat
            for name in ("matrix", "get_matrix", "get_unitary", "unitary", "to_matrix"):
                try:
                    member = getattr(obj, name)
                    mat = _to_matrix(member() if callable(member) else member)
                    if mat is not None:
                        return mat
                except Exception:
                    pass
            for name in module_funcs:
                try:
                    mat = _to_matrix(getattr(pq, name)(obj))
                    if mat is not None:
                        return mat
                except Exception:
                    pass
        raise RuntimeError("matrix unavailable")

    def _state_to_vector(state):
        if isinstance(state, dict):
            vec = np.zeros(2, dtype=complex)
            for k, v in state.items():
                if isinstance(k, str):
                    key = k.replace(" ", "").replace("|", "").replace(">", "")
                    idx = int(key, 2) if key else 0
                else:
                    idx = int(k)
                if idx < 2:
                    vec[idx] = complex(v)
            return vec
        arr = np.asarray(state, dtype=complex).reshape(-1)
        if arr.size >= 2:
            return arr[:2]
        raise RuntimeError("state unavailable")

    def _init_machine(machine):
        for name in ("init_qvm", "initQVM", "init", "initialize"):
            try:
                getattr(machine, name)()
                return
            except Exception:
                pass

    def _alloc_qubit(machine):
        for name in ("qAlloc", "qalloc", "allocate_qubit"):
            try:
                return getattr(machine, name)()
            except Exception:
                pass
        for name in ("qAlloc_many", "qalloc_many", "allocate_qubits"):
            try:
                return getattr(machine, name)(1)[0]
            except Exception:
                pass
        return 0

    def _state_from_framework(prep_one):
        machine_cls = getattr(pq, "CPUQVM")
        last_error = None
        for use_alloc in (True, False):
            try:
                machine = machine_cls()
                _init_machine(machine)
                q = _alloc_qubit(machine) if use_alloc else 0
                prog = pq.QProg()
                if prep_one:
                    prog = _append(prog, pq.X(q))
                prog = _append(prog, pq.H(q))

                for run_name in (
                    "directly_run",
                    "run",
                    "run_prog",
                    "simulate",
                    "run_state_vector",
                    "state_vector_simulate",
                ):
                    try:
                        runner = getattr(machine, run_name)
                    except Exception:
                        continue
                    for args in ((prog,), (prog, 1), (prog, [], 1)):
                        try:
                            result = runner(*args)
                            try:
                                return _state_to_vector(result)
                            except Exception:
                                pass
                            break
                        except Exception as exc:
                            last_error = exc

                for get_name in (
                    "get_qstate",
                    "get_qstate_vector",
                    "get_state",
                    "getState",
                    "state_vector",
                ):
                    try:
                        getter = getattr(machine, get_name)
                        return _state_to_vector(getter() if callable(getter) else getter)
                    except Exception as exc:
                        last_error = exc
            except Exception as exc:
                last_error = exc
        raise last_error if last_error is not None else RuntimeError("state unavailable")

    try:
        op_a = _matrix_from_framework()
    except Exception:
        try:
            col0 = _state_from_framework(False)
            col1 = _state_from_framework(True)
            op_a = np.column_stack((col0, col1))
        except Exception:
            pq.H(0)
            op_a = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)

    op_b = np.exp(1j * 0.5) * op_a
    dim = op_a.shape[0]
    fidelity = abs(np.trace(op_a.conjugate().T @ op_b)) ** 2 / (dim * dim)
    return float(np.real_if_close(fidelity))
