# EVAL_META: task_id=40, framework=cirq, class=1
import numpy as np
import cirq

def init_random_3qubit(desired_vector):
    qubits = cirq.LineQubit.range(3)
    state = np.asarray(desired_vector, dtype=np.complex128)
    state = state / np.linalg.norm(state)

    prep = cirq.StatePreparationChannel(state)
    circuit = cirq.Circuit()
    circuit.append(prep.on(*qubits))
    circuit.append(cirq.measure(*qubits, key='meas'))

    sim = cirq.Simulator(seed=42)
    reps = 4096
    result = sim.run(circuit, repetitions=reps)

    measurements = result.measurements['meas']
    counts = {}
    for row in measurements:
        bitstring = ''.join(str(int(b)) for b in row)
        counts[bitstring] = counts.get(bitstring, 0) + 1

    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
