# EVAL_META: task_id=40, framework=cirq, class=1
import numpy as np
import cirq

def init_random_3qubit(desired_vector):
    qubits = cirq.LineQubit.range(3)
    # Order chosen so that amplitude index mapping matches Qiskit little-endian
    order = [qubits[2], qubits[1], qubits[0]]
    state = np.asarray(desired_vector, dtype=complex)
    circuit = cirq.Circuit()
    circuit.append(cirq.StatePreparationChannel(state).on(*order))
    circuit.append(cirq.measure(*order, key='m'))
    sim = cirq.Simulator(seed=42)
    shots = 4096
    result = sim.run(circuit, repetitions=shots)
    measurements = result.measurements['m']
    counts = {}
    for row in measurements:
        key = ''.join(str(int(b)) for b in row)
        counts[key] = counts.get(key, 0) + 1
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
