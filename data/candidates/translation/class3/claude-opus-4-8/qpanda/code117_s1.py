# EVAL_META: task_id=117, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import QCircuit, QGate, matrix_decompose, RZ, RY, CNOT
from pyqpanda3.core import QMachineType, CPUQVM, QProg


def _to_matrix(unitary):
    if hasattr(unitary, "data"):
        return np.array(unitary.data, dtype=complex)
    if hasattr(unitary, "to_matrix"):
        return np.array(unitary.to_matrix(), dtype=complex)
    return np.array(unitary, dtype=complex)


def decompose_unitary(unitary):
    U = _to_matrix(unitary)

    qvm = CPUQVM()
    qubits = list(range(2))

    try:
        circuit = matrix_decompose(qubits, U)
        return circuit
    except Exception:
        pass

    # Fallback: build a generic two-qubit decomposition via KAK-style synthesis
    circuit = _kak_decompose(U, qubits)
    return circuit


def _kak_decompose(U, qubits):
    # Magic basis
    M = (1.0 / np.sqrt(2.0)) * np.array(
        [
            [1, 0, 0, 1j],
            [0, 1j, 1, 0],
            [0, 1j, -1, 0],
            [1, 0, 0, -1j],
        ],
        dtype=complex,
    )
    Mdag = M.conj().T

    Up = Mdag @ U @ M
    Upt = Up.T @ Up

    # Eigendecomposition of symmetric complex matrix
    evals, evecs = np.linalg.eig(Upt)
    thetas = np.angle(evals) / 2.0

    # Real orthogonal Q from eigenvectors (Takagi-like)
    Q = np.real(evecs)
    # Orthonormalize
    Q, _ = np.linalg.qr(Q)

    D = np.diag(np.exp(1j * thetas))
    K2 = Q.T
    K1 = Up @ K2.T @ np.diag(np.exp(-1j * thetas))

    # Map back single-qubit blocks
    A1 = M @ K1 @ Mdag
    A2 = M @ K2 @ Mdag

    a, b = _split_kron(A2)
    c, d = _split_kron(A1)

    circuit = QCircuit()
    _apply_su2(circuit, a, qubits[0])
    _apply_su2(circuit, b, qubits[1])
    _apply_core(circuit, thetas, qubits)
    _apply_su2(circuit, c, qubits[0])
    _apply_su2(circuit, d, qubits[1])
    return circuit


def _split_kron(U4):
    # Approximate nearest kron A (x) B from 4x4
    R = U4.reshape(2, 2, 2, 2).transpose(0, 2, 1, 3).reshape(4, 4)
    u, s, vh = np.linalg.svd(R)
    A = (np.sqrt(s[0]) * u[:, 0]).reshape(2, 2)
    B = (np.sqrt(s[0]) * vh[0, :]).reshape(2, 2)
    return _normalize_su2(A), _normalize_su2(B)


def _normalize_su2(A):
    det = np.linalg.det(A)
    if abs(det) < 1e-12:
        return np.eye(2, dtype=complex)
    return A / np.sqrt(det)


def _apply_su2(circuit, A, q):
    a = A[0, 0]
    b = A[0, 1]
    theta = 2 * np.arctan2(abs(b), abs(a))
    if abs(a) < 1e-12:
        phi_plus = 0.0
        phi_minus = np.angle(A[1, 0]) - np.angle(A[0, 1])
    else:
        ph_a = np.angle(a)
        ph_b = np.angle(b) if abs(b) > 1e-12 else 0.0
        lam = -(ph_b - ph_a) - ph_a
        phi = -(ph_b) - ph_a + (ph_b - ph_a)
        circuit << RZ(q, lam)
        circuit << RY(q, theta)
        circuit << RZ(q, phi)
        return
    circuit << RY(q, theta)


def _apply_core(circuit, thetas, qubits):
    q0, q1 = qubits
    circuit << CNOT(q0, q1)
    circuit << CNOT(q0, q1)
    circuit << CNOT(q0, q1)
