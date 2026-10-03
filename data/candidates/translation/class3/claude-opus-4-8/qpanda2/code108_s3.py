# EVAL_META: task_id=108, framework=qpanda2, class=3
import numpy as np
from pyqpanda import CPUQVM

machine = CPUQVM()
machine.init_qvm()


def _to_choi(data):
    arr = np.array(data, dtype=complex)
    dim2 = arr.shape[0]
    # If already a square Choi matrix
    if arr.ndim == 2 and arr.shape[0] == arr.shape[1]:
        d = int(round(np.sqrt(arr.shape[0])))
        if d * d == arr.shape[0]:
            # ambiguous: could be Choi (d^2 x d^2) or unitary (d x d)
            # Treat as unitary if it is unitary and not already choi-like:
            # Prefer interpreting as an operator/unitary of dimension arr.shape[0]
            pass
    # Interpret as a unitary/operator matrix U (d x d) -> Choi
    return _operator_to_choi(arr)


def _operator_to_choi(U):
    # U: d x d operator. Choi = sum_{i,j} |i><j| ⊗ (U|i><j|U^dagger)
    d = U.shape[0]
    choi = np.zeros((d * d, d * d), dtype=complex)
    for i in range(d):
        for j in range(d):
            eij = np.zeros((d, d), dtype=complex)
            eij[i, j] = 1.0
            mapped = U @ eij @ U.conj().T
            choi += np.kron(eij, mapped)
    return choi


def _choi_adjoint(choi, d):
    # Adjoint of a channel: reshape Choi and transpose the map
    # Choi_adjoint corresponds to the adjoint (dagger) map.
    C = choi.reshape(d, d, d, d)  # indices: i, k, j, l  (input i,j ; output k,l)
    # Choi element C[i,k,j,l] = <k| Lambda(|i><j|) |l>
    # Adjoint map Lambda^dagger: Choi^adj[j,l,i,k] = conj(C[i,k,j,l])
    Cadj = np.conjugate(np.transpose(C, (2, 3, 0, 1)))
    return Cadj.reshape(d * d, d * d)


def _choi_compose(choi1, choi2, d):
    # Compose: choi1 then choi2? Qiskit compose(other): self followed by other
    # choi1.compose(choi2) applies choi1 first, then choi2.
    C1 = choi1.reshape(d, d, d, d)  # <k|L1(|i><j|)|l> = C1[i,k,j,l]
    C2 = choi2.reshape(d, d, d, d)  # <n|L2(|k><l|)|m> = C2[k,n,l,m]
    # Composed L(|i><j|) = L2(L1(|i><j|))
    # L1(|i><j|) = sum_{k,l} C1[i,k,j,l] |k><l|
    # L2(|k><l|) = sum_{n,m} C2[k,n,l,m] |n><m|
    # So <n|L(|i><j|)|m> = sum_{k,l} C1[i,k,j,l] * C2[k,n,l,m]
    comp = np.einsum('ikjl,knlm->injm', C1, C2)
    return comp.reshape(d * d, d * d)


def initialize_adjoint_and_compose(data1, data2):
    choi1 = _to_choi(data1)
    choi2 = _to_choi(data2)
    d = int(round(np.sqrt(choi1.shape[0])))
    adjoint_choi1 = _choi_adjoint(choi1, d)
    composed_choi = _choi_compose(choi1, choi2, d)
    return choi1, adjoint_choi1, composed_choi


machine.finalize()
