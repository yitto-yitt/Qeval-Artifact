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
    original_program = pq.QProg()
    original_program << circuit
    original = np.asarray(pq.get_matrix(original_program), dtype=complex)
    dimension = math.isqrt(original.size)
    original = original.reshape(dimension, dimension)
    num_qubits = dimension.bit_length() - 1

    if dimension != 1 << num_qubits:
        raise ValueError("The circuit matrix must have power-of-two dimension.")
    if num_qubits > len(qubits):
        raise ValueError("The circuit exceeds the globally allocated qubit capacity.")

    rng = np.random.default_rng()

    def phase_normalize(matrix):
        index = int(np.argmax(np.abs(matrix).ravel() > 0.4))
        return matrix * np.exp(-1j * np.angle(matrix.flat[index]))

    original_normalized = phase_normalize(original)

    def random_clifford_circuit():
        result = pq.QCircuit()
        for qubit in qubits[:num_qubits]:
            result << pq.I(qubit)

        for offset in range(num_qubits):
            width = num_qubits - offset

            while True:
                first = rng.integers(0, 2, size=(2, width), dtype=np.int64)
                if np.any(first):
                    break

            while True:
                second = rng.integers(0, 2, size=(2, width), dtype=np.int64)
                pairing = (
                    np.dot(first[0], second[1])
                    + np.dot(first[1], second[0])
                ) % 2
                if pairing:
                    break

            paulis = np.stack((first, second))
            reduction = pq.QCircuit()

            def apply_h(index):
                reduction.insert(pq.H(qubits[offset + index]))
                temporary = paulis[:, 0, index].copy()
                paulis[:, 0, index] = paulis[:, 1, index]
                paulis[:, 1, index] = temporary

            def apply_s(index):
                reduction.insert(pq.S(qubits[offset + index]))
                paulis[:, 1, index] ^= paulis[:, 0, index]

            def apply_cnot(control, target):
                reduction.insert(
                    pq.CNOT(qubits[offset + control], qubits[offset + target])
                )
                paulis[:, 0, target] ^= paulis[:, 0, control]
                paulis[:, 1, control] ^= paulis[:, 1, target]

            for index in range(width):
                if paulis[0, 0, index]:
                    if paulis[0, 1, index]:
                        apply_s(index)
                    apply_h(index)

            pivot = int(np.flatnonzero(paulis[0, 1])[0])
            if pivot:
                apply_cnot(0, pivot)
                apply_cnot(pivot, 0)
                apply_cnot(0, pivot)

            for index in range(1, width):
                if paulis[0, 1, index]:
                    apply_cnot(index, 0)

            for index in range(1, width):
                x = paulis[1, 0, index]
                z = paulis[1, 1, index]
                if not (x or z):
                    continue
                if not x:
                    apply_h(index)
                elif z:
                    apply_s(index)
                apply_cnot(0, index)

            if paulis[1, 1, 0]:
                apply_s(0)

            combined = pq.QCircuit()
            combined << reduction.dagger() << result
            result = combined

        for qubit in qubits[:num_qubits]:
            if rng.integers(2):
                result << pq.X(qubit)
            if rng.integers(2):
                result << pq.Z(qubit)

        return result

    circuits = []
    while len(circuits) < n:
        candidate = random_clifford_circuit()
        program = pq.QProg()
        program << candidate
        matrix = np.asarray(pq.get_matrix(program), dtype=complex)
        matrix = matrix.reshape(dimension, dimension)

        if np.allclose(
            phase_normalize(matrix),
            original_normalized,
            rtol=0.4,
            atol=0.4,
        ):
            circuits.append(candidate)

    return circuits
