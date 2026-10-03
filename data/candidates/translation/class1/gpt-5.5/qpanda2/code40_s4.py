# EVAL_META: task_id=40, framework=qpanda2, class=1
import builtins
import numpy as np
import pyqpanda as pq

def init_random_3qubit(desired_vector):
    shots = 4096
    n_qubits = 3
    dim = 1 << n_qubits

    v = np.asarray(desired_vector, dtype=complex).reshape(dim)
    norm = np.linalg.norm(v)
    if norm == 0:
        raise ValueError("desired_vector must be non-zero")
    v = v / norm

    try:
        from pyqpanda.Algorithm.fragments import matrix_decompose as frag_matrix_decompose
    except Exception:
        frag_matrix_decompose = None

    qvm = pq.CPUQVM()
    qvm.init_qvm()

    def set_seed():
        for obj in (pq, qvm):
            setter = getattr(obj, "set_random_seed", None)
            if setter is not None:
                try:
                    setter(42)
                    return
                except Exception:
                    pass

    def nested_matrix(mat):
        return [[complex(mat[i, j]) for j in range(mat.shape[1])] for i in range(mat.shape[0])]

    def flat_matrix(mat):
        return [complex(mat[i, j]) for i in range(mat.shape[0]) for j in range(mat.shape[1])]

    def add_unitary(prog, qubits, mat):
        nested = nested_matrix(mat)
        flat = flat_matrix(mat)
        factories = []
        if hasattr(pq, "matrix_decompose"):
            factories.extend([
                lambda: pq.matrix_decompose(qubits, nested),
                lambda: pq.matrix_decompose(qubits, flat),
                lambda: pq.matrix_decompose(nested, qubits),
                lambda: pq.matrix_decompose(flat, qubits),
            ])
        if frag_matrix_decompose is not None:
            factories.extend([
                lambda: frag_matrix_decompose(qubits, nested),
                lambda: frag_matrix_decompose(qubits, flat),
                lambda: frag_matrix_decompose(nested, qubits),
                lambda: frag_matrix_decompose(flat, qubits),
            ])
        if hasattr(pq, "QOracle"):
            factories.extend([
                lambda: pq.QOracle(qubits, nested),
                lambda: pq.QOracle(qubits, flat),
                lambda: pq.QOracle(nested, qubits),
                lambda: pq.QOracle(flat, qubits),
            ])

        last_error = None
        for factory in factories:
            try:
                component = factory()
                if isinstance(component, tuple):
                    component = component[0]
                prog << component
                return
            except Exception as exc:
                last_error = exc
        if last_error is not None:
            raise last_error
        raise RuntimeError("No suitable pyQPanda unitary construction API is available")

    def complete_unitary(first_column):
        basis = [np.asarray(first_column, dtype=complex)]
        basis[0] = basis[0] / np.linalg.norm(basis[0])
        for i in range(dim):
            w = np.zeros(dim, dtype=complex)
            w[i] = 1.0
            for b in basis:
                w = w - b * np.vdot(b, w)
            w_norm = np.linalg.norm(w)
            if w_norm > 1e-12:
                basis.append(w / w_norm)
            if len(basis) == dim:
                break
        return np.column_stack(basis)

    def basis_unitary(index):
        mat = np.eye(dim, dtype=complex)
        if index != 0:
            mat[:, [0, index]] = mat[:, [index, 0]]
        return mat

    def add_measurements(prog, qubits, cbits):
        for i in range(n_qubits):
            prog << pq.Measure(qubits[i], cbits[i])

    def clean_key(key):
        return str(key).replace(" ", "").zfill(n_qubits)[-n_qubits:]

    def dominant_key(counts):
        return clean_key(max(counts.items(), key=lambda item: item[1])[0])

    try:
        set_seed()
        q = qvm.qAlloc_many(n_qubits)
        c = qvm.cAlloc_many(n_qubits)

        gate_raw = {}
        for index in range(dim):
            prog = pq.QProg()
            for bit in range(n_qubits):
                if (index >> bit) & 1:
                    prog << pq.X(q[bit])
            add_measurements(prog, q, c)
            counts = qvm.run_with_configuration(prog, c, 32)
            gate_raw[index] = dominant_key(counts)

        matrix_raw = {}
        for index in range(dim):
            prog = pq.QProg()
            add_unitary(prog, q, basis_unitary(index))
            add_measurements(prog, q, c)
            counts = qvm.run_with_configuration(prog, c, 32)
            matrix_raw[index] = dominant_key(counts)

        raw_to_matrix_index = {raw: index for index, raw in matrix_raw.items()}
        raw_to_qiskit_key = {raw: format(index, "03b") for index, raw in gate_raw.items()}

        qpanda_vector = np.zeros(dim, dtype=complex)
        for qiskit_index, amplitude in enumerate(v):
            raw = gate_raw[qiskit_index]
            matrix_index = raw_to_matrix_index.get(raw, qiskit_index)
            qpanda_vector[matrix_index] = amplitude

        unitary = complete_unitary(qpanda_vector)

        set_seed()
        prog = pq.QProg()
        add_unitary(prog, q, unitary)
        add_measurements(prog, q, c)
        raw_counts = qvm.run_with_configuration(prog, c, shots)

        counts = {}
        for raw_key, value in raw_counts.items():
            key = clean_key(raw_key)
            qiskit_key = raw_to_qiskit_key.get(key, key)
            counts[qiskit_key] = counts.get(qiskit_key, 0) + value

        total = builtins.sum(counts.values())
        return {key: value / total for key, value in counts.items() if value}
    finally:
        try:
            qvm.finalize()
        except Exception:
            pass
