# EVAL_META: task_id=40, framework=cirq, class=1
import cirq
from collections import Counter

def init_random_3qubit(desired_vector):
    qubits = cirq.LineQubit.range(3)
    circuit = cirq.Circuit(cirq.measure(*qubits, key='meas'))
    simulator = cirq.Simulator(seed=42)
    result = simulator.run(circuit, initial_state=desired_vector, repetitions=4096)
    meas = result.measurements['meas']
    bitstrings = [''.join(str(b) for b in row[::-1]) for row in meas]
    counts = Counter(bitstrings)
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
