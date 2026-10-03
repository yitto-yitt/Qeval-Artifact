# EVAL_META: task_id=40, framework=cirq, class=1
import cirq
import numpy as np

def init_random_3qubit(desired_vector):
    qubits = cirq.LineQubit.range(3)
    state = np.asarray(desired_vector, dtype=np.complex128)
    circuit = cirq.Circuit(
        cirq.StatePreparationChannel(state).on(*qubits),
        cirq.measure(*qubits, key='meas')
    )
    simulator = cirq.Simulator(seed=42)
    result = simulator.run(circuit, repetitions=4096)
    measurements = result.measurements['meas']
    counts = {}
    for row in measurements:
        bitstring = ''.join(str(int(bit)) for bit in row)
        counts[bitstring] = counts.get(bitstring, 0) + 1
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
