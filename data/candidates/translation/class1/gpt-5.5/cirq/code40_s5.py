# EVAL_META: task_id=40, framework=cirq, class=1
import cirq
import numpy as np

def init_random_3qubit(desired_vector):
    qubits = cirq.LineQubit.range(3)
    state = np.asarray(desired_vector, dtype=np.complex128).reshape(-1)
    norm = np.linalg.norm(state)
    if norm == 0:
        raise ValueError("desired_vector must be non-zero")
    state = state / norm

    n = state.size
    cols = [state]
    eye = np.eye(n, dtype=np.complex128)
    for j in range(n):
        w = eye[:, j].copy()
        for col in cols:
            w = w - col * np.vdot(col, w)
        w_norm = np.linalg.norm(w)
        if w_norm > 1e-12:
            cols.append(w / w_norm)
        if len(cols) == n:
            break

    unitary = np.column_stack(cols)
    circuit = cirq.Circuit(
        cirq.MatrixGate(unitary).on(*qubits),
        cirq.measure(*qubits, key="meas"),
    )

    simulator = cirq.Simulator(seed=42)
    result = simulator.run(circuit, repetitions=4096)
    measurements = result.measurements["meas"]

    counts = {}
    for row in measurements:
        bitstring = "".join(str(int(bit)) for bit in row)
        counts[bitstring] = counts.get(bitstring, 0) + 1

    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
