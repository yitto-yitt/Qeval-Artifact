# EVAL_META: task_id=139, framework=qiskit, class=2
import numpy as np
from qiskit.quantum_info import DensityMatrix, Statevector, schmidt_decomposition


def schmidt_test(data, qargs_B):
    try:
        return schmidt_decomposition(data, qargs_B)
    except Exception:
        try:
            return schmidt_decomposition(DensityMatrix(data), qargs_B)
        except Exception:
            arr = np.asarray(getattr(data, "data", data), dtype=complex)

            if arr.ndim == 1:
                psi = arr.astype(complex, copy=True)
            else:
                herm = (arr + arr.conj().T) / 2
                vals, vecs = np.linalg.eigh(herm)
                psi = vecs[:, int(np.argmax(vals.real))]
                pivot = int(np.argmax(np.abs(psi)))
                if np.abs(psi[pivot]) > 0:
                    psi = psi * np.exp(-1j * np.angle(psi[pivot]))

            try:
                dims = tuple(data.dims())
            except Exception:
                n = int(round(np.log2(psi.size)))
                dims = (2,) * n

            qargs_B = list(qargs_B)
            qargs_A = [i for i in range(len(dims)) if i not in qargs_B]

            dims_A = tuple(dims[i] for i in qargs_A)
            dims_B = tuple(dims[i] for i in qargs_B)
            dim_A = int(np.prod(dims_A, dtype=int)) if dims_A else 1
            dim_B = int(np.prod(dims_B, dtype=int)) if dims_B else 1

            mat = np.zeros((dim_A, dim_B), dtype=complex)

            for flat_index, amp in enumerate(psi):
                rem = flat_index
                local = []
                for d in dims:
                    local.append(rem % d)
                    rem //= d

                row = 0
                stride = 1
                for q in qargs_A:
                    row += local[q] * stride
                    stride *= dims[q]

                col = 0
                stride = 1
                for q in qargs_B:
                    col += local[q] * stride
                    stride *= dims[q]

                mat[row, col] = amp

            u, s, vh = np.linalg.svd(mat, full_matrices=False)
            tol = max(mat.shape) * np.finfo(float).eps * (s[0] if s.size else 0.0)

            terms = []
            for i, coeff in enumerate(s):
                if coeff > tol:
                    terms.append(
                        (
                            float(coeff),
                            Statevector(u[:, i], dims=dims_A if dims_A else (1,)),
                            Statevector(vh[i, :], dims=dims_B if dims_B else (1,)),
                        )
                    )
            return terms
