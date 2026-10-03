# EVAL_META: task_id=40, framework=qpanda2, class=1
import builtins
import numpy as np
import pyqpanda as pq

def init_random_3qubit(desired_vector):
    try:
        pq.set_random_seed(42)
    except Exception:
        pass

    shots = 4096
    n_qubits = 3
    dim = 1 << n_qubits

    vec = getattr(desired_vector, "data", desired_vector)
    vec = np.asarray(vec, dtype=np.complex128).reshape(-1)
    norm = np.linalg.norm(vec)
    if norm == 0:
        raise ValueError("desired_vector must be non-zero")
    vec = vec / norm

    def _unitary_with_first_column(col):
        col = np.asarray(col, dtype=np.complex128).reshape(-1)
        col = col / np.linalg.norm(col)
        cols = [col]
        size = len(col)
        for i in range(size):
            w = np.zeros(size, dtype=np.complex128)
            w[i] = 1.0
            for b in cols:
                w = w - b * np.vdot(b, w)
            w_norm = np.linalg.norm(w)
            if w_norm > 1e-12:
                cols.append(w / w_norm)
            if len(cols) == size:
                break
        return np.column_stack(cols).astype(np.complex128)

    def _basis_unitary(row):
        mat = np.eye(dim, dtype=np.complex128)
        if row != 0:
            mat[:, [0, row]] = mat[:, [row, 0]]
        return mat

    qvm = pq.CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(n_qubits)
    c = qvm.cAlloc_many(n_qubits)

    try:
        positions = {}
        for i in range(n_qubits):
            prog = pq.QProg()
            prog.insert(pq.X(q[i]))
            prog.insert(pq.measure_all(q, c))
            counts = qvm.run_with_configuration(prog, c, 32)
            raw_key = max(counts, key=counts.get)
            raw_key = str(raw_key).zfill(n_qubits)
            positions[i] = raw_key.index("1")

        def _to_qiskit_key(raw):
            raw = str(raw).zfill(n_qubits)
            return "".join(raw[positions[i]] for i in range(n_qubits - 1, -1, -1))

        qkey_to_row = {}
        for row in range(dim):
            prog = pq.QProg()
            prog.insert(pq.matrix_decompose(q, _basis_unitary(row)))
            prog.insert(pq.measure_all(q, c))
            counts = qvm.run_with_configuration(prog, c, 128)
            raw_key = max(counts, key=counts.get)
            qkey_to_row[_to_qiskit_key(raw_key)] = row

        target = np.zeros(dim, dtype=np.complex128)
        for idx, amp in enumerate(vec):
            qiskit_key = format(idx, "03b")
            target[qkey_to_row[qiskit_key]] = amp

        prog = pq.QProg()
        prog.insert(pq.matrix_decompose(q, _unitary_with_first_column(target)))
        prog.insert(pq.measure_all(q, c))

        counts = qvm.run_with_configuration(prog, c, shots)
        total = builtins.sum(counts.values())

        probabilities = {}
        for raw_key, count in counts.items():
            key = _to_qiskit_key(raw_key)
            probabilities[key] = probabilities.get(key, 0.0) + count / total

        return probabilities
    finally:
        qvm.finalize()
