# EVAL_META: task_id=110, framework=qpanda2, class=3
import atexit
import math
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(29)


def equivalent_clifford_circuit(circuit, n):
    def operator_matrix(node):
        program = pq.QProg()
        program << node
        matrix = np.asarray(pq.get_matrix(program), dtype=complex)
        dimension = math.isqrt(matrix.size)
        return matrix.reshape(dimension, dimension)

    original = operator_matrix(circuit)
    num_qubits = original.shape[0].bit_length() - 1
    if original.shape != (1 << num_qubits, 1 << num_qubits):
        raise ValueError("The circuit operator must have a power-of-two dimension.")
    if num_qubits > len(qubits):
        raise ValueError("The circuit exceeds the global quantum register.")

    rng = np.random.default_rng()
    results = []

    def random_clifford():
        layers = []

        for offset in range(num_qubits):
            width = num_qubits - offset
            while True:
                p = rng.integers(0, 2, size=2 * width, dtype=np.int64)
                if np.any(p):
                    break

            while True:
                q = rng.integers(0, 2, size=2 * width, dtype=np.int64)
                parity = (
                    np.dot(p[:width], q[width:])
                    + np.dot(p[width:], q[:width])
                ) & 1
                if parity:
                    break

            x = np.stack((p[:width], q[:width])).copy()
            z = np.stack((p[width:], q[width:])).copy()
            signs = rng.integers(0, 2, size=2, dtype=np.int64)
            layer = pq.QCircuit()

            def apply(gate, a, b=None):
                if gate == "H":
                    signs[:] ^= x[:, a] & z[:, a]
                    old_x = x[:, a].copy()
                    x[:, a] = z[:, a]
                    z[:, a] = old_x
                    layer << pq.H(qubits[offset + a])
                elif gate == "S":
                    signs[:] ^= x[:, a] & z[:, a]
                    z[:, a] ^= x[:, a]
                    layer << pq.S(qubits[offset + a])
                elif gate == "CNOT":
                    signs[:] ^= (
                        x[:, a] & z[:, b] & (x[:, b] ^ z[:, a] ^ 1)
                    )
                    x[:, b] ^= x[:, a]
                    z[:, a] ^= z[:, b]
                    layer << pq.CNOT(qubits[offset + a], qubits[offset + b])
                elif gate == "X":
                    signs[:] ^= z[:, a]
                    layer << pq.X(qubits[offset + a])
                elif gate == "Z":
                    signs[:] ^= x[:, a]
                    layer << pq.Z(qubits[offset + a])

            for j in range(width):
                if x[0, j]:
                    if z[0, j]:
                        apply("S", j)
                    apply("H", j)

            pivot = int(np.flatnonzero(z[0])[0])
            if pivot:
                apply("CNOT", 0, pivot)
                apply("CNOT", pivot, 0)
                apply("CNOT", 0, pivot)

            for j in range(1, width):
                if z[0, j]:
                    apply("CNOT", j, 0)

            for j in range(1, width):
                if x[1, j]:
                    apply("CNOT", 0, j)
                if z[1, j]:
                    apply("H", j)
                    apply("CNOT", 0, j)
                    apply("H", j)

            if z[1, 0]:
                apply("S", 0)
            if signs[0]:
                apply("X", 0)
            if signs[1]:
                apply("Z", 0)

            layers.append(layer.dagger())

        candidate = pq.QCircuit()
        for j in range(num_qubits):
            candidate << pq.I(qubits[j])
        for layer in reversed(layers):
            candidate << layer
        return candidate

    while len(results) < n:
        candidate = random_clifford()
        candidate_matrix = operator_matrix(candidate)
        reference_matrix = original

        nonzero = np.argwhere(np.abs(candidate_matrix) > 0.4)
        if nonzero.size:
            index = tuple(nonzero[0])
            candidate_matrix = candidate_matrix * np.exp(
                -1j * np.angle(candidate_matrix[index])
            )
            reference_matrix = reference_matrix * np.exp(
                -1j * np.angle(reference_matrix[index])
            )

        if np.allclose(candidate_matrix, reference_matrix, rtol=0.4, atol=0.4):
            results.append(candidate)

    return results


atexit.register(machine.finalize)
