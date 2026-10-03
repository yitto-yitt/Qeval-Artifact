# EVAL_META: task_id=139, framework=pennylane, class=2
import numpy as np

def schmidt_test(data, qargs_B):
    data = np.asarray(data)
    if data.ndim == 1:
        statevec = data
    elif data.ndim == 2:
        rho = data
        purity = np.trace(rho @ rho)
        if not np.isclose(purity, 1.0):
            raise ValueError("Input density matrix is not a pure state.")
        eigvals, eigvecs = np.linalg.eigh(rho)
        idx = np.argmax(eigvals)
        statevec = eigvecs[:, idx]
    else:
        raise ValueError("Input data must be a statevector or density matrix.")
    
    n = int(np.log2(len(statevec)))
    if 2**n != len(statevec):
        raise ValueError("Invalid statevector length.")
    
    qargs_B = list(qargs_B)
    if len(set(qargs_B)) != len(qargs_B):
        raise ValueError("qargs_B contains duplicate qubits.")
    if any(q < 0 or q >= n for q in qargs_B):
        raise ValueError("qargs_B contains invalid qubit indices.")
    
    qargs_A = [i for i in range(n) if i not in qargs_B]
    dim_A = 2 ** len(qargs_A)
    dim_B = 2 ** len(qargs_B)
    
    M = np.zeros((dim_A, dim_B), dtype=complex)
    for a in range(dim_A):
        for b in range(dim_B):
            full_index = 0
            for k, qubit in enumerate(qargs_A):
                bit = (a >> k) & 1
                full_index |= (bit << qubit)
            for k, qubit in enumerate(qargs_B):
                bit = (b >> k) & 1
                full_index |= (bit << qubit)
            M[a, b] = statevec[full_index]
    
    U, S, Vh = np.linalg.svd(M)
    
    ret = []
    for k in range(len(S)):
        coeff = S[k]
        state_A = U[:, k]
        state_B = Vh[k, :]
        ret.append((coeff, state_A, state_B))
    return ret
