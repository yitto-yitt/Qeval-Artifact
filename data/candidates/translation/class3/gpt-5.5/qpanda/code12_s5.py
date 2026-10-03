# EVAL_META: task_id=12, framework=qpanda, class=3
import numpy as np
import pyqpanda3.core as pq


def get_unitary():
    def _init_machine():
        m = pq.CPUQVM()
        for name in ("init", "init_qvm"):
            if hasattr(m, name):
                try:
                    getattr(m, name)()
                    break
                except Exception:
                    pass
        return m

    def _alloc_qubits(m, n):
        for name in ("qAlloc_many", "qalloc_many", "qAllocMany", "qallocMany", "allocate_qubits"):
            if hasattr(m, name):
                try:
                    return getattr(m, name)(n)
                except Exception:
                    pass
        for name in ("qAlloc", "qalloc", "allocate_qubit"):
            if hasattr(m, name):
                return [getattr(m, name)() for _ in range(n)]
        raise RuntimeError("Unable to allocate qubits")

    def _append(container, op):
        try:
            r = container << op
            return container if r is None else r
        except Exception:
            pass
        try:
            r = container.insert(op)
            return container if r is None else r
        except Exception:
            pass
        raise

    def _program(q, basis_index=0):
        prog = pq.QProg()
        if basis_index & 1:
            prog = _append(prog, pq.X(q[0]))
        if basis_index & 2:
            prog = _append(prog, pq.X(q[1]))
        prog = _append(prog, pq.H(q[0]))
        prog = _append(prog, pq.CNOT(q[0], q[1]))
        return prog

    def _run(m, prog):
        for name in ("directly_run", "run", "run_qprog"):
            if hasattr(m, name):
                try:
                    getattr(m, name)(prog)
                    return
                except Exception:
                    pass
        raise RuntimeError("Unable to run program")

    def _state(m):
        for name in ("get_qstate", "get_qstate_vector", "get_state"):
            if hasattr(m, name):
                try:
                    s = getattr(m, name)()
                    if isinstance(s, dict):
                        arr = np.zeros(4, dtype=complex)
                        for k, v in s.items():
                            idx = int(k, 2) if isinstance(k, str) else int(k)
                            if idx < 4:
                                arr[idx] = complex(v)
                        return arr
                    arr = np.asarray(s, dtype=complex).reshape(-1)
                    return arr[:4]
                except Exception:
                    pass
        if hasattr(pq, "get_qstate"):
            s = pq.get_qstate()
            return np.asarray(s, dtype=complex).reshape(-1)[:4]
        raise RuntimeError("Unable to get state")

    def _probe_little_endian():
        m = _init_machine()
        q = _alloc_qubits(m, 2)
        prog = pq.QProg()
        prog = _append(prog, pq.X(q[0]))
        _run(m, prog)
        s = _state(m)
        return abs(s[1]) >= abs(s[2])

    def _bitrev2(i):
        return ((i & 1) << 1) | ((i & 2) >> 1)

    try:
        little = _probe_little_endian()
        u = np.zeros((4, 4), dtype=complex)
        for col in range(4):
            m = _init_machine()
            q = _alloc_qubits(m, 2)
            prog = _program(q, col)
            _run(m, prog)
            s = _state(m)
            if little:
                u[:, col] = s[:4]
            else:
                for row in range(4):
                    u[row, col] = s[_bitrev2(row)]
        return u
    except Exception:
        pass

    def _matrix_of(obj):
        for name in ("get_matrix", "get_unitary"):
            if hasattr(pq, name):
                try:
                    a = np.asarray(getattr(pq, name)(obj), dtype=complex)
                    if a.ndim == 1:
                        a = a.reshape((4, 4))
                    return a
                except Exception:
                    pass
        for name in ("get_matrix", "matrix", "to_matrix"):
            if hasattr(obj, name):
                try:
                    a = np.asarray(getattr(obj, name)(), dtype=complex)
                    if a.ndim == 1:
                        a = a.reshape((4, 4))
                    return a
                except Exception:
                    pass
        raise RuntimeError("Unable to get matrix")

    m = _init_machine()
    q = _alloc_qubits(m, 2)
    circ = pq.QCircuit() if hasattr(pq, "QCircuit") else pq.QProg()
    circ = _append(circ, pq.H(q[0]))
    circ = _append(circ, pq.CNOT(q[0], q[1]))
    mat = _matrix_of(circ)

    probe = pq.QCircuit() if hasattr(pq, "QCircuit") else pq.QProg()
    probe = _append(probe, pq.CNOT(q[0], q[1]))
    try:
        pmat = _matrix_of(probe)
        big_cx = np.array(
            [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]],
            dtype=complex,
        )
        if np.allclose(pmat, big_cx):
            perm = np.array(
                [[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]],
                dtype=complex,
            )
            mat = perm @ mat @ perm.T
    except Exception:
        pass

    return mat
