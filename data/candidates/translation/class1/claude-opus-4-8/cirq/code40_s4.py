# EVAL_META: task_id=40, framework=cirq, class=1
import numpy as np
import cirq


def _unitary_from_state(v):
    v = np.asarray(v, dtype=complex)
    n = len(v)
    v = v / np.linalg.norm(v)
    M = np.zeros((n, n), dtype=complex)
    M[:, 0] = v
    idx = 1
    for e in range(n):
        vec = np.zeros(n, dtype=complex)
        vec[e] = 1.0
        for c in range(idx):
            vec -= np.vdot(M[:, c], vec) * M[:, c]
        norm = np.linalg.norm(vec)
        if norm > 1e-9:
            M[:, idx] = vec / norm
            idx += 1
        if idx == n:
            break
    return M


def init_random_3qubit(desired_vector):
    q = cirq.LineQubit.range(3)
    U = _unitary_from_state(desired_vector)
    gate = cirq.MatrixGate(U, qid_shape=(2, 2, 2))
    circuit = cirq.Circuit()
    circuit.append(gate.on(*q))
    circuit.append(cirq.measure(*q, key='m'))

    sim = cirq.Simulator(seed=42)
    reps = 4096
    result = sim.run(circuit, repetitions=reps)
    meas = result.measurements['m']

    counts = {}
    for row in meas:
        key = ''.join(str(int(b)) for b in row)
        counts[key] = counts.get(key, 0) + 1

    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
