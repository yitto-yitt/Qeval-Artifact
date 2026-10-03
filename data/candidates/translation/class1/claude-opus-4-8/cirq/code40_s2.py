# EVAL_META: task_id=40, framework=cirq, class=1
import numpy as np
import cirq

def init_random_3qubit(desired_vector):
    state = np.asarray(desired_vector, dtype=np.complex128)
    state = state / np.linalg.norm(state)

    q0, q1, q2 = cirq.LineQubit.range(3)

    circuit = cirq.Circuit()
    circuit.append(cirq.StatePreparationChannel(state).on(q2, q1, q0))
    circuit.append(cirq.measure(q2, q1, q0, key='meas'))

    shots = 4096
    simulator = cirq.Simulator(seed=42)
    result = simulator.run(circuit, repetitions=shots)

    meas = result.measurements['meas']
    counts = {}
    for row in meas:
        key = ''.join(str(int(b)) for b in row)
        counts[key] = counts.get(key, 0) + 1

    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
