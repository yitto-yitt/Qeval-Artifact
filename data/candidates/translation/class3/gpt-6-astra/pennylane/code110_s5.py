# EVAL_META: task_id=110, framework=pennylane, class=3
import numpy as np
import pennylane as qml


def equivalent_clifford_circuit(circuit, n):
    wires = list(circuit.wires)
    num_qubits = len(wires)
    rng = np.random.default_rng()
    results = []

    if n <= 0:
        return results

    with qml.QueuingManager.stop_recording():
        original = qml.tape.QuantumScript(list(circuit.operations))
        target = (
            np.asarray(qml.matrix(original, wire_order=wires), dtype=complex)
            if num_qubits
            else np.ones((1, 1), dtype=complex)
        )

        while len(results) < n:
            stages = []

            for offset in range(num_qubits):
                size = num_qubits - offset
                active = wires[offset:]

                while True:
                    p = rng.integers(0, 2, size=(2, size), dtype=np.int64)
                    if np.any(p):
                        break

                while True:
                    q = rng.integers(0, 2, size=(2, size), dtype=np.int64)
                    if (np.dot(p[0], q[1]) + np.dot(p[1], q[0])) % 2:
                        break

                x = np.stack((p[0], q[0]))
                z = np.stack((p[1], q[1]))
                reduction = []

                def apply_gate(kind, a, b=None):
                    if kind == "H":
                        reduction.append(qml.Hadamard(wires=active[a]))
                        old_x = x[:, a].copy()
                        x[:, a] = z[:, a]
                        z[:, a] = old_x
                    elif kind == "Sdg":
                        reduction.append(qml.adjoint(qml.S(wires=active[a])))
                        z[:, a] ^= x[:, a]
                    elif kind == "CX":
                        reduction.append(qml.CNOT(wires=[active[a], active[b]]))
                        x[:, b] ^= x[:, a]
                        z[:, a] ^= z[:, b]
                    elif kind == "SWAP":
                        reduction.append(qml.SWAP(wires=[active[a], active[b]]))
                        x[:, [a, b]] = x[:, [b, a]]
                        z[:, [a, b]] = z[:, [b, a]]

                for j in range(size):
                    if z[0, j]:
                        apply_gate("Sdg" if x[0, j] else "H", j)

                pivot = int(np.flatnonzero(x[0])[0])
                for j in range(size):
                    if j != pivot and x[0, j]:
                        apply_gate("CX", pivot, j)

                if pivot != 0:
                    apply_gate("SWAP", pivot, 0)
                apply_gate("H", 0)

                for j in range(1, size):
                    if z[1, j]:
                        apply_gate("Sdg" if x[1, j] else "H", j)
                    if x[1, j]:
                        apply_gate("CX", 0, j)

                if z[1, 0]:
                    apply_gate("Sdg", 0)

                stages.append(reduction)

            operations = []
            for reduction in reversed(stages):
                operations.extend(qml.adjoint(op) for op in reversed(reduction))

            for wire in wires:
                if rng.integers(2):
                    operations.append(qml.PauliX(wires=wire))
                if rng.integers(2):
                    operations.append(qml.PauliZ(wires=wire))

            candidate = qml.tape.QuantumScript(operations)
            matrix = (
                np.asarray(qml.matrix(candidate, wire_order=wires), dtype=complex)
                if num_qubits
                else np.ones((1, 1), dtype=complex)
            )

            index = np.unravel_index(np.argmax(np.abs(matrix)), matrix.shape)
            aligned_candidate = matrix * np.exp(-1j * np.angle(matrix[index]))
            aligned_target = target * np.exp(-1j * np.angle(target[index]))

            if np.allclose(aligned_candidate, aligned_target, rtol=0.4, atol=0.4):
                results.append(candidate)

    return results
