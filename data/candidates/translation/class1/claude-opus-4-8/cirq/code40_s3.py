# EVAL_META: task_id=40, framework=cirq, class=1
import numpy as np
import cirq

def init_random_3qubit(desired_vector):
    q = cirq.LineQubit.range(3)
    target = np.asarray(desired_vector, dtype=np.complex128)
    target = target / np.linalg.norm(target)

    circuit = cirq.Circuit()
    # Prepare state with q[0] as least-significant bit (Qiskit little-endian convention)
    circuit.append(cirq.StatePreparationChannel(target).on(q[2], q[1], q[0]))
    circuit.append(cirq.measure(q[2], q[1], q[0], key='m'))

    sim = cirq.Simulator(seed=42)
    shots = 4096
    result = sim.run(circuit, repetitions=shots)

    meas = result.measurements['m']  # columns correspond to q2, q1, q0
    counts = {}
    for row in meas:
        key = ''.join(str(int(b)) for b in row)
        counts[key] = counts.get(key, 0) + 1

    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
