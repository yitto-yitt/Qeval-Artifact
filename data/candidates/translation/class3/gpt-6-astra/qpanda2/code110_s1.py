# EVAL_META: task_id=110, framework=qpanda2, class=3
import atexit
import math
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(24)
atexit.register(lambda: machine.finalize())


def equivalent_clifford_circuit(circuit, n):
    target = np.asarray(
        pq.get_matrix(pq.QProg() << circuit), dtype=np.complex128
    )
    dimension = math.isqrt(target.size)
    if dimension * dimension != target.size or dimension == 0:
        raise ValueError("The input circuit must have a square unitary matrix.")
    target = target.reshape(dimension, dimension)
    num_qubits = dimension.bit_length() - 1
    if dimension != 1 << num_qubits:
        raise ValueError("The matrix dimension must be a power of two.")
    if num_qubits > len(qubits):
        raise ValueError("The circuit exceeds the global quantum register size.")

    rng = np.random.default_rng()
    pivot = np.unravel_index(np.argmax(np.abs(target)), target.shape)
    results = []

    while len(results) < n:
        reductions = []

        for start in range(num_qubits):
            width = num_qubits - start

            # Uniformly sample an ordered anticommuting Pauli pair.
            while True:
                p = rng.integers(0, 2, size=(2, width), dtype=np.int8)
                if np.any(p):
                    break
            while True:
                q = rng.integers(0, 2, size=(2, width), dtype=np.int8)
                parity = (
                    int(np.dot(p[0].astype(np.int64), q[1]))
                    + int(np.dot(p[1].astype(np.int64), q[0]))
                ) & 1
                if parity:
                    break

            xs = np.stack((p[0], q[0]))
            zs = np.stack((p[1], q[1]))
            reduction = pq.QCircuit()

            def apply_h(j):
                reduction.insert(pq.H(qubits[start + j]))
                old_x = xs[:, j].copy()
                xs[:, j] = zs[:, j]
                zs[:, j] = old_x

            def apply_s(j):
                reduction.insert(pq.S(qubits[start + j]))
                zs[:, j] ^= xs[:, j]

            def apply_cnot(control, target_index):
                reduction.insert(
                    pq.CNOT(
                        qubits[start + control],
                        qubits[start + target_index],
                    )
                )
                xs[:, target_index] ^= xs[:, control]
                zs[:, control] ^= zs[:, target_index]

            # Map the first Pauli to Z on the first remaining qubit.
            for j in range(width):
                if xs[0, j]:
                    if zs[0, j]:
                        apply_s(j)
                    apply_h(j)

            anchor = int(np.flatnonzero(zs[0])[0])
            if anchor:
                apply_cnot(anchor, 0)
                apply_cnot(0, anchor)
                apply_cnot(anchor, 0)

            for j in range(1, width):
                if zs[0, j]:
                    apply_cnot(j, 0)

            # Preserve that Z while mapping its partner to X.
            for j in range(1, width):
                if xs[1, j]:
                    if zs[1, j]:
                        apply_s(j)
                elif zs[1, j]:
                    apply_h(j)
                if xs[1, j]:
                    apply_cnot(0, j)

            if zs[1, 0]:
                apply_s(0)
            apply_h(0)
            reductions.append(reduction)

        candidate = pq.QCircuit()
        for j in range(num_qubits):
            candidate.insert(pq.I(qubits[j]))
        for reduction in reversed(reductions):
            candidate.insert(reduction.dagger())

        # Uniform Pauli factors supply the independent Clifford signs.
        for j in range(num_qubits):
            if rng.integers(2):
                candidate.insert(pq.X(qubits[j]))
            if rng.integers(2):
                candidate.insert(pq.Z(qubits[j]))

        actual = np.asarray(
            pq.get_matrix(pq.QProg() << candidate), dtype=np.complex128
        ).reshape(dimension, dimension)
        phase = np.angle(target[pivot]) - np.angle(actual[pivot])
        if np.allclose(
            actual * np.exp(1j * phase), target, rtol=0.4, atol=0.4
        ):
            results.append(candidate)

    return results
