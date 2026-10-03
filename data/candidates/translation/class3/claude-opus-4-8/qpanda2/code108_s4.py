# EVAL_META: task_id=108, framework=qpanda2, class=3
import numpy as np
from pyqpanda import CPUQVM

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(4)


def _to_choi(data):
    data = np.asarray(data, dtype=complex)
    dim = data.shape[0]
    d = int(round(np.sqrt(dim)))
    if d * d == dim and data.shape[0] == data.shape[1]:
        # Heuristic: distinguish Choi (already d^2 x d^2) from unitary/superop.
        # Treat square matrix whose dimension is a perfect square as a superoperator
        # only if it is not itself already a Choi. We instead build Choi from a
        # unitary/operator when dimension is a perfect square of an integer d
        # such that d is the operator dimension.
        pass
    return data


def _operator_to_choi(op):
    op = np.asarray(op, dtype=complex)
    d = op.shape[0]
    choi = np.zeros((d * d, d * d), dtype=complex)
    for i in range(d):
        for j in range(d):
            # |i><j| input basis
            eij = np.zeros((d, d), dtype=complex)
            eij[i, j] = 1.0
            out = op @ eij @ op.conj().T
            # column-stacking convention (Qiskit uses column-vectorization)
            choi += np.kron(eij, out)
    return choi


def _superop_to_choi(sop, d):
    # sop is d^2 x d^2 superoperator in column-stacking convention.
    choi = np.zeros((d * d, d * d), dtype=complex)
    for i in range(d):
        for j in range(d):
            eij = np.zeros((d, d), dtype=complex)
            eij[i, j] = 1.0
            vec_in = eij.reshape(-1, order='F')
            vec_out = sop @ vec_in
            out = vec_out.reshape(d, d, order='F')
            choi += np.kron(eij, out)
    return choi


def _make_choi(data):
    arr = np.asarray(data, dtype=complex)
    n = arr.shape[0]
    m = arr.shape[1] if arr.ndim == 2 else 0
    # Determine representation.
    r = int(round(np.sqrt(n)))
    if arr.ndim == 2 and n == m and r * r == n:
        # Ambiguous: could be Choi (d^2 x d^2) or a d-dim operator when n is a
        # perfect square. Qiskit's Choi(data) with a square operator of size n
        # treats it as an operator (unitary) of dimension n. So build Choi from
        # operator of dimension n.
        return _operator_to_choi(arr)
    if arr.ndim == 2 and n == m:
        # Square operator, not perfect square dim -> unitary/operator.
        return _operator_to_choi(arr)
    return arr


def _choi_adjoint(choi, d):
    # Adjoint channel: Choi of adjoint. For Choi matrix C with row/col indexed
    # by (input, output) in column-stacking, adjoint swaps roles and conjugates.
    C = choi.reshape(d, d, d, d)  # indices: i_in, i_out, j_in, j_out (F-order kron)
    # Reconstruct via superoperator for robustness.
    sop = _choi_to_superop(choi, d)
    sop_adj = sop.conj().T
    return _superop_to_choi(sop_adj, d)


def _choi_to_superop(choi, d):
    # Convert Choi to superoperator (column-stacking).
    sop = np.zeros((d * d, d * d), dtype=complex)
    C = choi.reshape(d, d, d, d)  # from kron(eij, out): [i_in,i_out? ...]
    # kron(A,B): index = (a*d + b). Here choi += kron(eij, out).
    # rows/cols of choi index = (input_idx*d + output_idx).
    # Rebuild sop element S[(o1,o2),(i1,i2)] = <o1| Phi(|i1><i2|) |o2>
    for i1 in range(d):
        for i2 in range(d):
            for o1 in range(d):
                for o2 in range(d):
                    row = i1 * d + o1
                    col = i2 * d + o2
                    val = choi[row, col]
                    s_row = o2 * d + o1  # column-stacking vec(rho)_ab = rho[a,b] at index b*d+a
                    s_col = i2 * d + i1
                    sop[s_row, s_col] += val
    return sop


def _choi_dim(choi):
    n = choi.shape[0]
    return int(round(np.sqrt(n)))


def _compose(choi1, choi2, d):
    s1 = _choi_to_superop(choi1, d)
    s2 = _choi_to_superop(choi2, d)
    # Qiskit compose: choi1.compose(choi2) applies choi1 first, then choi2.
    composed = s2 @ s1
    return _superop_to_choi(composed, d)


def initialize_adjoint_and_compose(data1, data2):
    choi1 = _make_choi(data1)
    choi2 = _make_choi(data2)
    d = _choi_dim(choi1)
    adjoint_choi1 = _choi_adjoint(choi1, d)
    composed_choi = _compose(choi1, choi2, d)
    machine.finalize()
    return choi1, adjoint_choi1, composed_choi
