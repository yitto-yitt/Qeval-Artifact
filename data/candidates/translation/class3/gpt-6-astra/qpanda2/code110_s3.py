# EVAL_META: task_id=110, framework=qpanda2, class=3
import atexit
import random
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(32)


def equivalent_clifford_circuit(circuit, n):
    source_program = pq.QProg()
    source_program << circuit
    width = len(pq.get_all_used_qubits(source_program))

    if width > len(qubits):
        raise ValueError("The circuit exceeds the allocated qubit capacity.")
    if width == 0:
        return [pq.QCircuit(circuit) for _ in range(max(0, n))]

    reference = np.asarray(pq.get_matrix(source_program), dtype=complex).reshape(-1)
    rng = random.Random()

    def random_clifford():
        reductions = []

        for offset in range(width):
            size = width - offset

            while True:
                p = [rng.randrange(4) for _ in range(size)]
                if any(p):
                    break

            px = [v & 1 for v in p]
            pz = [v >> 1 for v in p]

            while True:
                q = [rng.randrange(4) for _ in range(size)]
                qx = [v & 1 for v in q]
                qz = [v >> 1 for v in q]
                if sum(
                    (px[i] & qz[i]) ^ (pz[i] & qx[i])
                    for i in range(size)
                ) % 2:
                    break

            reduction = pq.QCircuit()

            def apply(name, i, j=None):
                gate = getattr(pq, name)
                if j is None:
                    reduction.insert(gate(qubits[offset + i]))
                else:
                    reduction.insert(
                        gate(qubits[offset + i], qubits[offset + j])
                    )

                for x, z in ((px, pz), (qx, qz)):
                    if name == "H":
                        x[i], z[i] = z[i], x[i]
                    elif name == "S":
                        z[i] ^= x[i]
                    elif name == "CNOT":
                        x[j] ^= x[i]
                        z[i] ^= z[j]
                    elif name == "CZ":
                        z[i] ^= x[j]
                        z[j] ^= x[i]
                    elif name == "SWAP":
                        x[i], x[j] = x[j], x[i]
                        z[i], z[j] = z[j], z[i]

            for i in range(size):
                if px[i]:
                    if pz[i]:
                        apply("S", i)
                    apply("H", i)

            pivot = next(i for i in range(size) if pz[i])
            if pivot:
                apply("SWAP", 0, pivot)

            for i in range(1, size):
                if pz[i]:
                    apply("CNOT", i, 0)

            for i in range(1, size):
                if qx[i]:
                    apply("CNOT", 0, i)
                if qz[i]:
                    apply("CZ", 0, i)

            if qz[0]:
                apply("S", 0)

            reductions.append(reduction)

        candidate = pq.QCircuit()
        for i in range(width):
            candidate << pq.I(qubits[i])

        for reduction in reversed(reductions):
            candidate << reduction.dagger()

        for i in range(width):
            if rng.getrandbits(1):
                candidate << pq.X(qubits[i])
            if rng.getrandbits(1):
                candidate << pq.Z(qubits[i])

        return candidate

    results = []
    while len(results) < n:
        candidate = random_clifford()
        program = pq.QProg()
        program << candidate
        matrix = np.asarray(pq.get_matrix(program), dtype=complex).reshape(-1)

        pivot = int(np.argmax(np.abs(matrix)))
        aligned_candidate = matrix * np.exp(-1j * np.angle(matrix[pivot]))
        aligned_reference = reference * np.exp(-1j * np.angle(reference[pivot]))

        if np.allclose(
            aligned_candidate, aligned_reference, rtol=0.4, atol=0.4
        ):
            results.append(candidate)

    return results


atexit.register(lambda: machine.finalize())
