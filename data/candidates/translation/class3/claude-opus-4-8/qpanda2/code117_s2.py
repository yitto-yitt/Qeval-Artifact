# EVAL_META: task_id=117, framework=qpanda2, class=3
import numpy as np
from pyqpanda import CPUQVM, QCircuit, QProg
from pyqpanda import RZ, RY, CNOT
import pyqpanda as pq

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)


def _closest_unitary(A):
    V, _, Wh = np.linalg.svd(A)
    return V @ Wh


def _zyz(U):
    # decompose 2x2 unitary into RZ(alpha) RY(theta) RZ(beta) up to global phase
    U = np.array(U, dtype=complex)
    det = np.linalg.det(U)
    phase = det ** 0.5
    su = U / phase
    theta = 2 * np.arctan2(abs(su[1, 0]), abs(su[0, 0]))
    ang0 = np.angle(su[1, 1])
    ang1 = np.angle(su[1, 0])
    alpha = ang0 + ang1
    beta = ang0 - ang1
    return alpha, theta, beta


def _apply_single(circ, q, U):
    alpha, theta, beta = _zyz(U)
    circ << RZ(q, beta) << RY(q, theta) << RZ(q, alpha)


def _magic_basis():
    return (1 / np.sqrt(2)) * np.array([
        [1, 0, 0, 1j],
        [0, 1j, 1, 0],
        [0, 1j, -1, 0],
        [1, 0, 0, -1j],
    ], dtype=complex)


def decompose_unitary(unitary):
    U = np.array(unitary, dtype=complex)
    U = _closest_unitary(U)

    # Global phase normalization
    det = np.linalg.det(U)
    U = U / (det ** 0.25)

    # Compute the KAK / canonical decomposition of the two-qubit gate.
    B = _magic_basis()
    Bd = B.conj().T
    Um = Bd @ U @ B

    M2 = Um.T @ Um
    # Diagonalize M2 (symmetric complex) to get the two-qubit local gates
    # Use eigendecomposition
    D, P = np.linalg.eig(M2)

    # Ensure P is real orthogonal
    # Make eigenvectors real
    for i in range(4):
        v = P[:, i]
        # rotate to make largest component real
        idx = np.argmax(np.abs(v))
        v = v * np.exp(-1j * np.angle(v[idx]))
        P[:, i] = v.real + 0j
    # Orthonormalize
    P, _ = np.linalg.qr(P)

    # eigenvalues -> canonical parameters
    d = np.angle(D) / 2

    # K1, K2 in magic basis
    diag = np.exp(1j * d)
    # Reconstruct
    K2m = P.T
    K1m = Um @ P @ np.diag(np.exp(-1j * d))

    K1 = B @ K1m @ Bd
    K2 = B @ K2m @ Bd

    def _split(K):
        # K = kron(A, B) up to phase
        K = np.array(K, dtype=complex)
        # find nonzero block to extract factors
        n = 0
        best = 0
        for i in range(2):
            for j in range(2):
                block = K[2 * i:2 * i + 2, 2 * j:2 * j + 2]
                nv = np.linalg.norm(block)
                if nv > best:
                    best = nv
                    bi, bj = i, j
        block = K[2 * bi:2 * bi + 2, 2 * bj:2 * bj + 2]
        # factor
        Bfac = block / np.sqrt(np.abs(np.linalg.det(block)))
        # A entries
        Afac = np.zeros((2, 2), dtype=complex)
        for i in range(2):
            for j in range(2):
                blk = K[2 * i:2 * i + 2, 2 * j:2 * j + 2]
                Afac[i, j] = np.trace(blk @ Bfac.conj().T) / 2
        return Afac, Bfac

    # This full KAK is complex; fall back to building the exact circuit
    # via a robust generic 2-qubit decomposition using scipy-free approach.
    # Instead, construct circuit that reproduces U using the canonical form.
    a1, b1 = _split(K1)
    a2, b2 = _split(K2)

    dvals = np.sort(d)
    # canonical coefficients
    tx = (d[0] + d[1]) / 1
    # Use the interaction parameters
    c = d

    circ = QCircuit()
    # Apply K2 locals
    _apply_single(circ, qubits[0], a2)
    _apply_single(circ, qubits[1], b2)

    # Nonlocal part: implement exp(i(cx XX + cy YY + cz ZZ)) via 3 CNOTs
    cx = (c[0] + c[3])
    cy = (c[1] + c[2])
    cz = (c[0] + c[1])

    # Standard 3-CNOT canonical interaction circuit
    circ << CNOT(qubits[1], qubits[0])
    _apply_single(circ, qubits[0], np.array([[np.exp(-1j * cz), 0], [0, np.exp(1j * cz)]]))
    circ << RZ(qubits[0], -2 * cz)
    circ << RY(qubits[1], 2 * cx - np.pi / 2)
    circ << CNOT(qubits[0], qubits[1])
    circ << RY(qubits[1], np.pi / 2 - 2 * cy)
    circ << CNOT(qubits[1], qubits[0])

    # Apply K1 locals
    _apply_single(circ, qubits[0], a1)
    _apply_single(circ, qubits[1], b1)

    prog = QProg()
    prog << circ
    return prog
