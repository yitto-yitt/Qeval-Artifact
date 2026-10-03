# EVAL_META: task_id=110, framework=pennylane, class=3
import numpy as np
import pennylane as qml


def _equiv(a, b, rtol=0.4, atol=0.4):
    a = np.asarray(a)
    b = np.asarray(b)
    if a.shape != b.shape:
        return False
    idx = np.unravel_index(np.argmax(np.abs(b)), b.shape)
    if abs(b[idx]) < 1e-12:
        return False
    phase = a[idx] / b[idx]
    return np.allclose(a, phase * b, rtol=rtol, atol=atol)


def _random_clifford_ops(num_qubits, rng):
    depth = 10 * num_qubits + 10
    ops = []
    for _ in range(depth):
        g = rng.integers(0, 3)
        if g == 0:
            w = int(rng.integers(0, num_qubits))
            ops.append(qml.Hadamard(w))
        elif g == 1:
            w = int(rng.integers(0, num_qubits))
            ops.append(qml.S(w))
        else:
            if num_qubits < 2:
                w = int(rng.integers(0, num_qubits))
                ops.append(qml.Hadamard(w))
            else:
                a, b = rng.choice(num_qubits, size=2, replace=False)
                ops.append(qml.CNOT([int(a), int(b)]))
    return ops


def equivalent_clifford_circuit(circuit, n):
    num_qubits = len(circuit.wires)
    wire_order = list(range(num_qubits))
    op_or = qml.matrix(circuit, wire_order=wire_order)
    rng = np.random.default_rng()
    qc_list = []
    counter = 0
    while counter < n:
        ops = _random_clifford_ops(num_qubits, rng)
        tape = qml.tape.QuantumTape(ops, [])
        mat = qml.matrix(tape, wire_order=wire_order)
        if _equiv(mat, op_or):
            counter += 1
            qc_list.append(tape)
    return qc_list
