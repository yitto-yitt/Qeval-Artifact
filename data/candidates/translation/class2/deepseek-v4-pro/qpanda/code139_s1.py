# EVAL_META: task_id=139, framework=qpanda, class=2
import numpy as np

def schmidt_test(data, qargs_B):
    # Convert input to numpy array
    data = np.asarray(data, dtype=complex)
    if data.ndim == 1:
        # Pure state
        vec = data
        N = len(vec)
        n = int(np.round(np.log2(N)))
        if 2**n != N:
            raise ValueError("Length of vector must be a power of 2")
        qargs_B = list(qargs_B)
        # Validate qubit indices
        if any(q >= n or q < 0 for q in qargs_B):
            raise ValueError("Invalid qubit index in qargs_B")
        # Determine subsystem qubits
        all_q = set(range(n))
        A_qubits = sorted(list(all_q - set(qargs_B)))
        B_qubits = sorted(qargs_B)
        dimA = 2 ** len(A_qubits)
        dimB = 2 ** len(B_qubits)
        # Reshape and transpose to separate A and B subspaces
        shape = (2,) * n
        tensor = vec.reshape(shape)
        new_order = A_qubits + B_qubits
        tensor = np.transpose(tensor, axes=new_order)
        # Reshape to matrix of size (dimA, dimB) and SVD
        matrix = tensor.reshape(dimA, dimB)
        U, S, Vh = np.linalg.svd(matrix, full_matrices=False)
        # Extract Schmidt vectors
        V = Vh.conj().T  # columns are right-singular vectors
        result = []
        for i in range(len(S)):
            coeff = S[i]  # singular value (real, non-negative)
            state_A = U[:, i]
            state_B = V[:, i]
            result.append((coeff, state_A, state_B))
        return result

    elif data.ndim == 2:
        # Density matrix
        rho = data
        d = rho.shape[0]
        if rho.shape[1] != d:
            raise ValueError("Density matrix must be square")
        n = int(np.round(np.log2(d)))
        if 2**n != d:
            raise ValueError("Dimension must be a power of 2")
        qargs_B = list(qargs_B)
        if any(q >= n or q < 0 for q in qargs_B):
            raise ValueError("Invalid qubit index in qargs_B")
        all_q = set(range(n))
        A_qubits = sorted(list(all_q - set(qargs_B)))
        B_qubits = sorted(qargs_B)
        dimA = 2 ** len(A_qubits)
        dimB = 2 ** len(B_qubits)

        # Reshape rho into a tensor with 2*n indices: row qubits then column qubits
        shape = (2,) * n + (2,) * n
        rho_tensor_full = rho.reshape(shape)
        # Permute indices to group A row, B row, A col, B col
        new_order = []
        for q in A_qubits:
            new_order.append(q)            # row A
        for q in B_qubits:
            new_order.append(q)            # row B
        for q in A_qubits:
            new_order.append(q + n)        # col A
        for q in B_qubits:
            new_order.append(q + n)        # col B
        rho_tensor = np.transpose(rho_tensor_full, axes=new_order)
        # Now reshape to (dimA, dimB, dimA, dimB)
        rho_tensor = rho_tensor.reshape(dimA, dimB, dimA, dimB)

        # Partial trace over B to obtain rho_A
        rho_A = np.trace(rho_tensor, axis1=1, axis2=3)  # shape (dimA, dimA)

        # Diagonalize rho_A
        vals, vecs = np.linalg.eigh(rho_A)   # vals sorted ascending, vecs columns
        # Sort descending by eigenvalues
        idx = np.argsort(vals)[::-1]
        vals = vals[idx]
        vecs = vecs[:, idx]

        result = []
        for i in range(len(vals)):
            coeff = vals[i]  # eigenvalue (real)
            state_A = vecs[:, i]
            # Compute projected B-matrix
            # M_{b1,b2} = sum_{a1,a2} rho_{a1,b1,a2,b2} * conj(vecs[i][a1]) * vecs[i][a2]
            M = np.einsum('a,abcd,c->bd', state_A.conj(), rho_tensor, state_A)
            # Diagonalize M to find state_B
            eigvals_M, eigvecs_M = np.linalg.eigh(M)
            id_max = np.argmax(eigvals_M)
            state_B = eigvecs_M[:, id_max]
            result.append((coeff, state_A, state_B))
        return result

    else:
        raise ValueError("Input must be a 1D statevector or a 2D density matrix")
