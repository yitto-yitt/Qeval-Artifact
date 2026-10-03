# EVAL_META: task_id=40, framework=cirq, class=1
import cirq

def init_random_3qubit(desired_vector):
    qubits = cirq.LineQubit.range(3)
    circuit = cirq.Circuit(
        cirq.StatePreparationGate(desired_vector).on(*reversed(qubits)),
        cirq.measure(*qubits, key='meas')
    )
    simulator = cirq.Simulator(seed=42)
    result = simulator.run(circuit, repetitions=1024)
    measurements = result.measurements['meas']
    counts = {}
    for sample in measurements:
        bitstring = ''.join(str(bit) for bit in reversed(sample))
        counts[bitstring] = counts.get(bitstring, 0) + 1
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
