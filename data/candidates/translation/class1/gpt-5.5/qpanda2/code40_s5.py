# EVAL_META: task_id=40, framework=qpanda2, class=1
import builtins
import numpy as np
import pyqpanda as pq

def init_random_3qubit(desired_vector):
    if isinstance(desired_vector, np.ndarray):
        data = desired_vector
    elif hasattr(desired_vector, "data") and not isinstance(desired_vector, (list, tuple)):
        data = desired_vector.data
    else:
        data = desired_vector

    vec = np.asarray(data, dtype=complex).reshape(-1)
    if vec.size != 8:
        raise ValueError("desired_vector must contain 8 amplitudes for 3 qubits")

    norm = np.linalg.norm(vec)
    if norm == 0:
        raise ValueError("desired_vector must be non-zero")
    vec = vec / norm

    cols = [vec]
    for i in range(8):
        e = np.zeros(8, dtype=complex)
        e[i] = 1.0
        w = e.copy()
        for c in cols:
            w = w - np.vdot(c, w) * c
        w_norm = np.linalg.norm(w)
        if w_norm > 1e-12:
            cols.append(w / w_norm)
        if len(cols) == 8:
            break
    unitary = np.column_stack(cols)

    flat = [complex(x) for x in unitary.reshape(-1)]
    nested = [[complex(unitary[i, j]) for j in range(8)] for i in range(8)]

    matrix_candidates = []
    if hasattr(pq, "QStat"):
        try:
            matrix_candidates.append(pq.QStat(flat))
        except Exception:
            pass
    matrix_candidates.extend([flat, nested, unitary])

    qvm = pq.CPUQVM()
    qvm.init_qvm()
    try:
        qubits = qvm.qAlloc_many(3)

        circuit = None
        last_error = None
        md = getattr(pq, "matrix_decompose", None)
        if md is not None:
            for mat in matrix_candidates:
                try:
                    circuit = md(qubits, mat)
                    break
                except Exception as exc:
                    last_error = exc
                try:
                    tmp_circuit = pq.QCircuit()
                    ret = md(qubits, mat, tmp_circuit)
                    circuit = tmp_circuit if ret is None or isinstance(ret, bool) else ret
                    break
                except Exception as exc:
                    last_error = exc

        if circuit is None and hasattr(pq, "QOracle"):
            qo = getattr(pq, "QOracle")
            for mat in matrix_candidates:
                try:
                    circuit = qo(qubits, mat)
                    break
                except Exception as exc:
                    last_error = exc
                try:
                    circuit = qo(mat, qubits)
                    break
                except Exception as exc:
                    last_error = exc

        if circuit is None:
            raise last_error if last_error is not None else RuntimeError("Unable to construct state initialization circuit")

        prog = pq.QProg()
        prog << circuit
        qvm.directly_run(prog)
        state = qvm.get_qstate()

        probs = {}
        for i, amp in enumerate(state[:8]):
            p = abs(complex(amp)) ** 2
            if p > 1e-12:
                probs[format(i, "03b")] = float(p)

        total = builtins.sum(probs.values())
        if total != 0:
            probs = {k: v / total for k, v in probs.items()}
        return probs
    finally:
        try:
            qvm.finalize()
        except Exception:
            pass
