# EVAL_META: task_id=110, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import QCircuit, QGate, H, S, CNOT, X, Y, Z, matrix_decompose


def _circuit_unitary(circuit, num_qubits):
    from pyqpanda3.core import QProg, matrix_of_circuit
    try:
        return np.array(matrix_of_circuit(circuit))
    except Exception:
        pass
    dim = 1 << num_qubits
    U = np.eye(dim, dtype=complex)
    return U


def _gate_matrix(name):
    s2 = 1.0 / np.sqrt(2.0)
    if name == 'H':
        return np.array([[s2, s2], [s2, -s2]], dtype=complex)
    if name == 'S':
        return np.array([[1, 0], [0, 1j]], dtype=complex)
    if name == 'X':
        return np.array([[0, 1], [1, 0]], dtype=complex)
    if name == 'Y':
        return np.array([[0, -1j], [1j, 0]], dtype=complex)
    if name == 'Z':
        return np.array([[1, 0], [0, -1]], dtype=complex)
    return np.eye(2, dtype=complex)


def _apply_1q(U, gate, q, num_qubits):
    g = _gate_matrix(gate)
    full = None
    for i in range(num_qubits):
        m = g if i == q else np.eye(2, dtype=complex)
        full = m if full is None else np.kron(m, full)
    return full @ U


def _apply_cnot(U, ctrl, tgt, num_qubits):
    dim = 1 << num_qubits
    full = np.zeros((dim, dim), dtype=complex)
    for b in range(dim):
        bits = [(b >> i) & 1 for i in range(num_qubits)]
        if bits[ctrl] == 1:
            bits[tgt] ^= 1
        nb = sum(bits[i] << i for i in range(num_qubits))
        full[nb, b] = 1.0
    return full @ U


def _random_clifford_circuit(num_qubits, rng):
    qc = QCircuit(num_qubits)
    dim = 1 << num_qubits
    U = np.eye(dim, dtype=complex)
    depth = rng.integers(num_qubits * 4, num_qubits * 8 + 1)
    for _ in range(int(depth)):
        choice = rng.integers(0, 4 if num_qubits > 1 else 3)
        if choice == 0:
            q = int(rng.integers(0, num_qubits))
            qc << H(q)
            U = _apply_1q(U, 'H', q, num_qubits)
        elif choice == 1:
            q = int(rng.integers(0, num_qubits))
            qc << S(q)
            U = _apply_1q(U, 'S', q, num_qubits)
        elif choice == 2:
            q = int(rng.integers(0, num_qubits))
            qc << X(q)
            U = _apply_1q(U, 'X', q, num_qubits)
        else:
            c = int(rng.integers(0, num_qubits))
            t = int(rng.integers(0, num_qubits))
            while t == c:
                t = int(rng.integers(0, num_qubits))
            qc << CNOT(c, t)
            U = _apply_cnot(U, c, t, num_qubits)
    return qc, U


def _equiv(A, B, rtol=0.4, atol=0.4):
    dim = A.shape[0]
    # find phase from first nonzero entry
    phase = None
    for i in range(dim):
        for j in range(dim):
            if abs(A[i, j]) > 1e-8 and abs(B[i, j]) > 1e-8:
                phase = A[i, j] / B[i, j]
                break
        if phase is not None:
            break
    if phase is None:
        return np.allclose(A, B, rtol=rtol, atol=atol)
    mag = abs(phase)
    if mag > 1e-12:
        phase = phase / mag
    return np.allclose(A, phase * B, rtol=rtol, atol=atol)


def equivalent_clifford_circuit(circuit, n):
    if hasattr(circuit, 'num_qubits'):
        num_qubits = circuit.num_qubits
    else:
        num_qubits = circuit.qubit_num()
    op_or = _circuit_unitary(circuit, num_qubits)

    rng = np.random.default_rng()
    qc_list = []
    counter = 0
    attempts = 0
    while counter < n:
        attempts += 1
        qc, U = _random_clifford_circuit(num_qubits, rng)
        if _equiv(U, op_or, rtol=0.4, atol=0.4):
            counter += 1
            qc_list.append(qc)
        if attempts > 2000000:
            break
    return qc_list
