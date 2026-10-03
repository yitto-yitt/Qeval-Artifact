# EVAL_META: task_id=110, framework=qpanda2, class=3
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
_global_qubits = machine.qAlloc_many(16)

def equivalent_clifford_circuit(circuit, n):
    target_mat = np.array(circuit, dtype=complex)
    if target_mat.ndim != 2 or target_mat.shape[0] != target_mat.shape[1]:
        raise ValueError("circuit must be a square unitary matrix-like object")
    dim = target_mat.shape[0]
    num_qubits = int(round(np.log2(dim)))
    if 2 ** num_qubits != dim:
        raise ValueError("matrix dimension must be a power of 2")
    if num_qubits > len(_global_qubits):
        raise ValueError("not enough globally allocated qubits")

    qubits = _global_qubits[:num_qubits]
    out = []

    while len(out) < n:
        prog = pq.QProg()
        depth = np.random.randint(1, 8)
        for _ in range(depth):
            gate_type = np.random.choice(["H", "S", "X", "Y", "Z", "CNOT"])
            if gate_type == "H":
                q = qubits[np.random.randint(0, num_qubits)]
                prog << pq.H(q)
            elif gate_type == "S":
                q = qubits[np.random.randint(0, num_qubits)]
                prog << pq.S(q)
            elif gate_type == "X":
                q = qubits[np.random.randint(0, num_qubits)]
                prog << pq.X(q)
            elif gate_type == "Y":
                q = qubits[np.random.randint(0, num_qubits)]
                prog << pq.Y(q)
            elif gate_type == "Z":
                q = qubits[np.random.randint(0, num_qubits)]
                prog << pq.Z(q)
            else:
                if num_qubits >= 2:
                    i, j = np.random.choice(num_qubits, 2, replace=False)
                    prog << pq.CNOT(qubits[i], qubits[j])
                else:
                    q = qubits[0]
                    prog << pq.H(q)

        cand_mat = np.array(pq.get_matrix(prog), dtype=complex)
        if cand_mat.shape != target_mat.shape:
            continue

        idx = np.unravel_index(np.argmax(np.abs(target_mat)), target_mat.shape)
        if np.abs(cand_mat[idx]) < 1e-12:
            continue
        phase = target_mat[idx] / cand_mat[idx]
        aligned = cand_mat * phase
        if np.allclose(aligned, target_mat, rtol=0.4, atol=0.4):
            out.append(prog)

    machine.finalize()
    return out
