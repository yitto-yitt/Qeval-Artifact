# EVAL_META: task_id=12, framework=qpanda, class=3
import numpy as np
import pyqpanda3.core as pq


def get_unitary():
    def _init_machine():
        qvm = None
        for name in ("CPUQVM", "CPUSingleThreadQVM"):
            cls = getattr(pq, name, None)
            if cls is not None:
                try:
                    qvm = cls()
                    break
                except Exception:
                    pass
        if qvm is None:
            raise RuntimeError("No supported QVM found")
        for name in ("init_qvm", "initQVM", "init"):
            method = getattr(qvm, name, None)
            if method is not None:
                try:
                    method()
                    break
                except Exception:
                    pass
        return qvm

    def _alloc_qubits(qvm, n):
        for name in ("qAlloc_many", "qalloc_many", "qAllocMany", "qallocMany", "allocate_qubits"):
            method = getattr(qvm, name, None)
            if method is not None:
                try:
                    return list(method(n))
                except Exception:
                    pass
        for name in ("qAlloc", "qalloc", "allocate_qubit"):
            method = getattr(qvm, name, None)
            if method is not None:
                qs = []
                for _ in range(n):
                    qs.append(method())
                return qs
        raise RuntimeError("No supported qubit allocator found")

    def _make_prog(q, x_mask=None):
        prog = pq.QProg()
        if x_mask is not None:
            if x_mask & 1:
                prog << pq.X(q[0])
            if x_mask & 2:
                prog << pq.X(q[1])
        prog << pq.H(q[0])
        prog << pq.CNOT(q[0], q[1])
        return prog

    def _matrix_from_framework(obj):
        for name in ("get_matrix", "get_unitary", "get_unitary_matrix"):
            fn = getattr(pq, name, None)
            if fn is not None:
                try:
                    m = np.asarray(fn(obj), dtype=complex)
                    if m.size == 16:
                        return m.reshape((4, 4))
                except Exception:
                    pass
        method = getattr(obj, "get_matrix", None)
        if method is not None:
            m = np.asarray(method(), dtype=complex)
            if m.size == 16:
                return m.reshape((4, 4))
        raise RuntimeError("No supported matrix extractor found")

    qvm = _init_machine()
    q = _alloc_qubits(qvm, 2)

    try:
        prog = _make_prog(q)
        mat = _matrix_from_framework(prog)

        xprog = pq.QProg()
        xprog << pq.X(q[0])
        xmat = _matrix_from_framework(xprog)
        mapped_index = int(np.argmax(np.abs(xmat[:, 0])))
        if mapped_index == 2:
            perm = [0, 2, 1, 3]
            mat = mat[np.ix_(perm, perm)]
        return mat
    except Exception:
        cols = []
        order_probe = None
        for basis in range(4):
            qvm_b = _init_machine()
            qb = _alloc_qubits(qvm_b, 2)
            prog_b = _make_prog(qb, basis)
            ran = False
            for name in ("directly_run", "run", "run_qprog"):
                method = getattr(qvm_b, name, None)
                if method is not None:
                    try:
                        method(prog_b)
                        ran = True
                        break
                    except Exception:
                        pass
            if not ran:
                raise
            state = None
            for name in ("get_qstate", "get_qsate", "get_qstate_vector", "get_state"):
                method = getattr(qvm_b, name, None)
                if method is not None:
                    try:
                        state = np.asarray(method(), dtype=complex)[:4]
                        break
                    except Exception:
                        pass
            if state is None:
                raise
            cols.append(state)

            if order_probe is None:
                qvm_p = _init_machine()
                qp = _alloc_qubits(qvm_p, 2)
                pprog = pq.QProg()
                pprog << pq.X(qp[0])
                for name in ("directly_run", "run", "run_qprog"):
                    method = getattr(qvm_p, name, None)
                    if method is not None:
                        try:
                            method(pprog)
                            break
                        except Exception:
                            pass
                for name in ("get_qstate", "get_qsate", "get_qstate_vector", "get_state"):
                    method = getattr(qvm_p, name, None)
                    if method is not None:
                        try:
                            pst = np.asarray(method(), dtype=complex)[:4]
                            order_probe = int(np.argmax(np.abs(pst)))
                            break
                        except Exception:
                            pass

        mat = np.column_stack(cols)
        if order_probe == 2:
            perm = [0, 2, 1, 3]
            mat = mat[np.ix_(perm, perm)]
        return mat
