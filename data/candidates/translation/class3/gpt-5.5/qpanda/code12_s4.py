# EVAL_META: task_id=12, framework=qpanda, class=3
import numpy as np
import pyqpanda3.core as pq


def get_unitary():
    def _new_container():
        last_exc = None
        for name in ("QProg", "QCircuit"):
            cls = getattr(pq, name, None)
            if cls is None:
                continue
            for args in ((), (2,)):
                try:
                    return cls(*args)
                except Exception as exc:
                    last_exc = exc
        if last_exc is not None:
            raise last_exc
        raise RuntimeError("No pyQPanda3 circuit container available")

    def _append(container, op):
        try:
            res = container << op
            return container if res is None else res
        except Exception:
            pass
        for name in ("insert", "push_back", "append", "add"):
            method = getattr(container, name, None)
            if callable(method):
                try:
                    res = method(op)
                    return container if res is None else res
                except Exception:
                    pass
        raise RuntimeError("Unable to append operation to pyQPanda3 program")

    def _build_main(q0, q1, prefix_mask=0):
        prog = _new_container()
        if prefix_mask & 1:
            prog = _append(prog, pq.X(q0))
        if prefix_mask & 2:
            prog = _append(prog, pq.X(q1))
        prog = _append(prog, pq.H(q0))
        prog = _append(prog, pq.CNOT(q0, q1))
        return prog

    def _build_x(q0, q1, which):
        prog = _new_container()
        if which == 0:
            prog = _append(prog, pq.X(q0))
            prog = _append(prog, pq.H(q1))
            prog = _append(prog, pq.H(q1))
        else:
            prog = _append(prog, pq.X(q1))
            prog = _append(prog, pq.H(q0))
            prog = _append(prog, pq.H(q0))
        return prog

    def _as_matrix(obj):
        if obj is None:
            return None
        try:
            arr = np.asarray(obj, dtype=complex)
        except Exception:
            return None
        if arr.shape == (4, 4):
            return arr
        if arr.size == 16:
            return arr.reshape((4, 4))
        return None

    def _extract_matrix(prog, q0=None, q1=None):
        names = (
            "get_unitary",
            "get_matrix",
            "get_qprog_matrix",
            "get_qprog_unitary",
            "get_circuit_matrix",
            "getCircuitMatrix",
            "get_matrix_from_prog",
            "get_unitary_matrix",
        )
        for name in names:
            fn = getattr(pq, name, None)
            if callable(fn):
                for args in ((prog,), (prog, True), (prog, [q0, q1]), (prog, [q0, q1], True)):
                    try:
                        mat = _as_matrix(fn(*args))
                        if mat is not None:
                            return mat
                    except Exception:
                        pass
        for name in names + ("matrix", "to_matrix", "unitary"):
            method = getattr(prog, name, None)
            if callable(method):
                for args in ((), (True,), ([q0, q1],), ([q0, q1], True)):
                    try:
                        mat = _as_matrix(method(*args))
                        if mat is not None:
                            return mat
                    except Exception:
                        pass
        return None

    def _qiskit_permutation_from_x(x0, x1):
        if x0 is None or x1 is None:
            return None
        i0 = int(np.argmax(np.abs(x0[:, 0])))
        i1 = int(np.argmax(np.abs(x1[:, 0])))
        if i0 not in (1, 2) or i1 not in (1, 2) or i0 == i1:
            return None
        return [0, i0, i1, i0 + i1]

    def _to_qiskit_order(mat, q0, q1):
        x0 = _extract_matrix(_build_x(q0, q1, 0), q0, q1)
        x1 = _extract_matrix(_build_x(q0, q1, 1), q0, q1)
        perm = _qiskit_permutation_from_x(x0, x1)
        if perm is None:
            return mat
        return mat[np.ix_(perm, perm)]

    def _make_qvm():
        qvm = pq.CPUQVM()
        for name in ("init_qvm", "initQVM", "init"):
            method = getattr(qvm, name, None)
            if callable(method):
                try:
                    method()
                    break
                except Exception:
                    pass

        for name in ("qAlloc_many", "qalloc_many", "qAllocMany", "allocate_qubits"):
            method = getattr(qvm, name, None)
            if callable(method):
                try:
                    qs = method(2)
                    return qvm, qs[0], qs[1]
                except Exception:
                    pass

        for name in ("qAlloc", "qalloc", "allocate_qubit"):
            method = getattr(qvm, name, None)
            if callable(method):
                try:
                    return qvm, method(), method()
                except Exception:
                    pass

        return qvm, 0, 1

    def _as_state(obj):
        if obj is None:
            return None
        if isinstance(obj, dict):
            return None
        try:
            arr = np.asarray(obj, dtype=complex).reshape(-1)
        except Exception:
            return None
        if arr.size >= 4:
            return arr[:4]
        return None

    def _simulate_state(mask):
        qvm, q0, q1 = _make_qvm()
        prog = _build_main(q0, q1, mask)

        run_result = None
        for name in ("directly_run", "run", "execute", "run_qprog", "run_prog"):
            method = getattr(qvm, name, None)
            if callable(method):
                try:
                    run_result = method(prog)
                    break
                except Exception:
                    pass

        state = _as_state(run_result)
        if state is None:
            for name in ("get_qstate", "get_q_state", "get_state", "getQState", "state"):
                method = getattr(qvm, name, None)
                if callable(method):
                    for args in ((), ([q0, q1],)):
                        try:
                            state = _as_state(method(*args))
                            if state is not None:
                                break
                        except Exception:
                            pass
                    if state is not None:
                        break

        finalize = getattr(qvm, "finalize", None)
        if callable(finalize):
            try:
                finalize()
            except Exception:
                pass

        if state is None:
            raise RuntimeError("Unable to retrieve statevector from pyQPanda3")
        return state

    def _simulate_unitary():
        sx0_qvm, _, _ = _make_qvm()
        try:
            x0_state = None
            x1_state = None

            def _simulate_x(which):
                qvm, q0, q1 = _make_qvm()
                prog = _new_container()
                prog = _append(prog, pq.X(q0 if which == 0 else q1))
                run_result = None
                for name in ("directly_run", "run", "execute", "run_qprog", "run_prog"):
                    method = getattr(qvm, name, None)
                    if callable(method):
                        try:
                            run_result = method(prog)
                            break
                        except Exception:
                            pass
                state = _as_state(run_result)
                if state is None:
                    for name in ("get_qstate", "get_q_state", "get_state", "getQState", "state"):
                        method = getattr(qvm, name, None)
                        if callable(method):
                            try:
                                state = _as_state(method())
                                if state is not None:
                                    break
                            except Exception:
                                pass
                finalize = getattr(qvm, "finalize", None)
                if callable(finalize):
                    try:
                        finalize()
                    except Exception:
                        pass
                return state

            x0_state = _simulate_x(0)
            x1_state = _simulate_x(1)
            if x0_state is not None and x1_state is not None:
                i0 = int(np.argmax(np.abs(x0_state)))
                i1 = int(np.argmax(np.abs(x1_state)))
                if i0 in (1, 2) and i1 in (1, 2) and i0 != i1:
                    perm = [0, i0, i1, i0 + i1]
                else:
                    perm = [0, 1, 2, 3]
            else:
                perm = [0, 1, 2, 3]
        finally:
            finalize = getattr(sx0_qvm, "finalize", None)
            if callable(finalize):
                try:
                    finalize()
                except Exception:
                    pass

        cols = []
        for mask in range(4):
            native_state = _simulate_state(mask)
            cols.append(native_state[perm])
        return np.column_stack(cols)

    built = []
    try:
        q0, q1 = 0, 1
        prog = _build_main(q0, q1)
        built.append((prog, q0, q1))
    except Exception:
        pass

    try:
        qvm, q0, q1 = _make_qvm()
        prog = _build_main(q0, q1)
        built.append((prog, q0, q1))
    except Exception:
        pass

    for prog, q0, q1 in built:
        mat = _extract_matrix(prog, q0, q1)
        if mat is not None:
            return _to_qiskit_order(mat, q0, q1)

    return _simulate_unitary()
