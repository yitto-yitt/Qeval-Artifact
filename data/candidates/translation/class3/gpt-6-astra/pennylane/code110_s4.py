# EVAL_META: task_id=110, framework=pennylane, class=3
import numpy as np
import pennylane as qml


def equivalent_clifford_circuit(circuit, n):
    if isinstance(circuit, qml.QNode):
        circuit = qml.workflow.construct_tape(circuit)()
    elif callable(circuit):
        circuit = qml.tape.make_qscript(circuit)()
    elif not isinstance(circuit, qml.tape.QuantumScript):
        circuit = qml.tape.QuantumScript(list(circuit))

    wires = list(circuit.wires)
    num_qubits = len(wires)
    original = np.asarray(
        qml.matrix(circuit, wire_order=wires), dtype=complex
    )
    rng = np.random.default_rng()

    def random_clifford_gates(start):
        size = num_qubits - start
        if size == 0:
            return []

        while True:
            p = rng.integers(0, 2, size=2 * size, dtype=np.int8)
            if np.any(p):
                break

        while True:
            q = rng.integers(0, 2, size=2 * size, dtype=np.int8)
            if (np.dot(p[:size], q[size:]) +
                    np.dot(p[size:], q[:size])) % 2:
                break

        x = np.stack((p[:size], q[:size]))
        z = np.stack((p[size:], q[size:]))
        reductions = []

        def apply(name, a, b=None):
            indices = (start + a,) if b is None else (start + a, start + b)
            reductions.append((name, indices))
            if name == "H":
                old_x = x[:, a].copy()
                x[:, a] = z[:, a]
                z[:, a] = old_x
            elif name == "S":
                z[:, a] ^= x[:, a]
            elif name == "CX":
                x[:, b] ^= x[:, a]
                z[:, a] ^= z[:, b]
            elif name == "SWAP":
                x[:, [a, b]] = x[:, [b, a]]
                z[:, [a, b]] = z[:, [b, a]]

        for j in range(size):
            if x[0, j]:
                if z[0, j]:
                    apply("S", j)
                apply("H", j)

        pivot = int(np.flatnonzero(z[0])[0])
        if pivot:
            apply("SWAP", 0, pivot)

        for j in range(1, size):
            if z[0, j]:
                apply("CX", j, 0)

        if z[1, 0]:
            apply("S", 0)

        for j in range(1, size):
            if z[1, j]:
                if x[1, j]:
                    apply("S", j)
                else:
                    apply("H", j)
            if x[1, j]:
                apply("CX", 0, j)

        gates = random_clifford_gates(start + 1)
        if rng.integers(2):
            gates.append(("X", (start,)))
        if rng.integers(2):
            gates.append(("Z", (start,)))

        gates.extend(
            ("Sdg" if name == "S" else name, indices)
            for name, indices in reversed(reductions)
        )
        return gates

    def make_tape(gates):
        operations = []
        constructors = {
            "H": qml.Hadamard,
            "X": qml.PauliX,
            "Z": qml.PauliZ,
            "CX": qml.CNOT,
            "SWAP": qml.SWAP,
        }
        with qml.QueuingManager.stop_recording():
            for name, indices in gates:
                gate_wires = [wires[i] for i in indices]
                if name == "Sdg":
                    operations.append(qml.adjoint(qml.S)(wires=gate_wires))
                else:
                    operations.append(constructors[name](wires=gate_wires))
        return qml.tape.QuantumScript(operations)

    results = []
    while len(results) < n:
        candidate = make_tape(random_clifford_gates(0))
        matrix = np.asarray(
            qml.matrix(candidate, wire_order=wires), dtype=complex
        )
        index = np.unravel_index(np.argmax(np.abs(matrix)), matrix.shape)
        aligned_candidate = matrix * np.exp(-1j * np.angle(matrix[index]))
        aligned_original = original * np.exp(-1j * np.angle(original[index]))
        if np.allclose(
            aligned_candidate, aligned_original, rtol=0.4, atol=0.4
        ):
            results.append(candidate)

    return results
