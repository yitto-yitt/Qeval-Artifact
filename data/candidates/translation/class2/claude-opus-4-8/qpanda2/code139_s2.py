# EVAL_META: task_id=139, framework=qpanda2, class=2
import numpy as np
from qiskit.quantum_info import Statevector


def schmidt_test(data, qargs_B):
    state = Statevector(data)
    sv = state.data
    dims = state.dims()
    num_qubits = len(dims)

    qargs_B = sorted(qargs_B)
    qargs_A = [q for q in range(num_qubits) if q not in qargs_B]

    dim_A = int(np.prod([dims[q] for q in qargs_A])) if qargs_A else 1
    dim_B = int(np.prod([dims[q] for q in qargs_B])) if qargs_B else 1

    def index_of(a_vals, b_vals):
        idx = 0
        for q in range(num_qubits):
            if q in qargs_A:
                pos = qargs_A.index(q)
                bit = a_vals[pos]
            else:
                pos = qargs_B.index(q)
                bit = b_vals[pos]
            idx += bit * (2 ** q)
        return idx

    def to_bits(val, qlist):
        bits = []
        for q in qlist:
            bits.append((val // (2 ** 0)) )
        return bits

    def decode(val, qlist):
        res = []
        for i in range(len(qlist)):
            res.append((val >> i) & 1)
        return res

    M = np.zeros((dim_A, dim_B), dtype=complex)
    for a in range(dim_A):
        a_vals = decode(a, qargs_A)
        for b in range(dim_B):
            b_vals = decode(b, qargs_B)
            M[a, b] = sv[index_of(a_vals, b_vals)]

    U, S, Vh = np.linalg.svd(M)

    terms = []
    for k in range(len(S)):
        coeff = S[k]
        if coeff < 1e-12:
            continue
        vecA = U[:, k]
        vecB = Vh[k, :].conj()
        terms.append((coeff, Statevector(vecA), Statevector(vecB)))

    return terms
