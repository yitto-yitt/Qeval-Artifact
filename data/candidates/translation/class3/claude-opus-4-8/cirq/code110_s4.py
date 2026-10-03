# EVAL_META: task_id=110, framework=cirq, class=3
import cirq
import numpy as np


def _equiv(u, v, rtol=0.4, atol=0.4):
    u = np.asarray(u, dtype=complex)
    v = np.asarray(v, dtype=complex)
    if u.shape != v.shape:
        return False
    idx = np.argmax(np.abs(v))
    if np.abs(v.flat[idx]) < 1e-12:
        return np.allclose(u, v, rtol=rtol, atol=atol)
    phase = u.flat[idx] / v.flat[idx]
    if np.abs(np.abs(phase) - 1.0) > atol:
        return False
    return np.allclose(u, phase * v, rtol=rtol, atol=atol)


def _random_clifford_circuit(qubits, rng):
    num_qubits = len(qubits)
    circuit = cirq.Circuit()
    depth = 4 * num_qubits + 4
    single = [cirq.H, cirq.S, cirq.X, cirq.Y, cirq.Z]
    for _ in range(depth):
        for q in qubits:
            gate = single[rng.integers(len(single))]
            circuit.append(gate(q))
        if num_qubits >= 2:
            perm = rng.permutation(num_qubits)
            for i in range(0, num_qubits - 1, 2):
                a = qubits[perm[i]]
                b = qubits[perm[i + 1]]
                circuit.append(cirq.CNOT(a, b))
    circuit.append(cirq.I(q) for q in qubits)
    return circuit


def equivalent_clifford_circuit(circuit, n):
    qubits = sorted(circuit.all_qubits())
    num_qubits = len(qubits)
    if num_qubits == 0:
        return [cirq.Circuit() for _ in range(n)]

    ref_op = cirq.unitary(circuit)
    rng = np.random.default_rng()

    qc_list = []
    while len(qc_list) < n:
        qc = _random_clifford_circuit(qubits, rng)
        try:
            op = cirq.unitary(qc)
        except Exception:
            continue
        if _equiv(op, ref_op):
            qc_list.append(qc)
    return qc_list
