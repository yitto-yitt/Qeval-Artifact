# EVAL_META: task_id=110, framework=pennylane, class=3
import numpy as np
import pennylane as qml


def equivalent_clifford_circuit(circuit, n):
    if isinstance(circuit, qml.QNode):
        tape = qml.workflow.construct_tape(circuit)()
        wires = list(circuit.device.wires or tape.wires)
    elif isinstance(circuit, qml.tape.QuantumScript):
        tape = circuit
        wires = list(tape.wires)
    elif callable(circuit):
        tape = qml.tape.make_qscript(circuit)()
        wires = list(tape.wires)
    else:
        tape = qml.tape.QuantumScript(list(circuit))
        wires = list(tape.wires)

    target = np.asarray(
        qml.matrix(
            qml.tape.QuantumScript(tape.operations),
            wire_order=wires,
        ),
        dtype=complex,
    )
    rng = np.random.default_rng()
    matrix_cache = {}
    dimension = 2 ** len(wires)

    def random_clifford_operations(active_wires):
        k = len(active_wires)
        if k == 0:
            return []

        while True:
            px, pz = rng.integers(0, 2, size=(2, k))
            if np.any(px | pz):
                break

        while True:
            qx, qz = rng.integers(0, 2, size=(2, k))
            if (np.dot(px, qz) + np.dot(pz, qx)) % 2:
                break

        reduction = []
        support = px | pz

        for j, wire in enumerate(active_wires):
            if px[j]:
                if pz[j]:
                    reduction.append(qml.adjoint(qml.S(wire), lazy=False))
                    qz[j] ^= qx[j]
                reduction.append(qml.Hadamard(wire))
                qx[j], qz[j] = qz[j], qx[j]

        pivot = int(np.flatnonzero(support)[0])
        if pivot:
            reduction.append(qml.SWAP([active_wires[0], active_wires[pivot]]))
            support[[0, pivot]] = support[[pivot, 0]]
            qx[[0, pivot]] = qx[[pivot, 0]]
            qz[[0, pivot]] = qz[[pivot, 0]]

        for j in range(1, k):
            if support[j]:
                reduction.append(qml.CNOT([active_wires[j], active_wires[0]]))
                qx[0] ^= qx[j]
                qz[j] ^= qz[0]

        for j in range(1, k):
            if qx[j]:
                if qz[j]:
                    reduction.append(
                        qml.adjoint(qml.S(active_wires[j]), lazy=False)
                    )
                    qz[j] ^= qx[j]
                reduction.append(qml.Hadamard(active_wires[j]))
                qx[j], qz[j] = qz[j], qx[j]
            if qz[j]:
                reduction.append(qml.CZ([active_wires[0], active_wires[j]]))
                qz[0] ^= qx[j]
                qz[j] ^= qx[0]

        if qz[0]:
            reduction.append(qml.adjoint(qml.S(active_wires[0]), lazy=False))

        operations = random_clifford_operations(active_wires[1:])
        if rng.integers(2):
            operations.append(qml.PauliX(active_wires[0]))
        if rng.integers(2):
            operations.append(qml.PauliZ(active_wires[0]))
        operations.extend(
            qml.adjoint(operation, lazy=False)
            for operation in reversed(reduction)
        )
        return operations

    results = []
    with qml.QueuingManager.stop_recording():
        while len(results) < n:
            operations = random_clifford_operations(wires)
            candidate = np.eye(dimension, dtype=complex)

            for operation in operations:
                key = (operation.name, tuple(operation.wires))
                if key not in matrix_cache:
                    matrix_cache[key] = np.asarray(
                        qml.matrix(operation, wire_order=wires),
                        dtype=complex,
                    )
                candidate = matrix_cache[key] @ candidate

            pivot = np.unravel_index(
                np.argmax(np.abs(candidate)), candidate.shape
            )
            candidate_aligned = candidate * np.exp(
                -1j * np.angle(candidate[pivot])
            )
            target_aligned = target * np.exp(-1j * np.angle(target[pivot]))

            if np.allclose(
                candidate_aligned, target_aligned, rtol=0.4, atol=0.4
            ):
                if not operations and wires:
                    operations = [qml.Identity(wire) for wire in wires]
                results.append(qml.tape.QuantumScript(operations))

    return results
