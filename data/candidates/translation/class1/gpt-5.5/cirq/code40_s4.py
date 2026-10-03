# EVAL_META: task_id=40, framework=cirq, class=1
import cirq
from collections import Counter

def init_random_3qubit(desired_vector):
    qubits = cirq.LineQubit.range(3)
    circuit = cirq.Circuit()
    circuit.append(cirq.StatePreparationChannel(desired_vector).on(qubits[2], qubits[1], qubits[0]))
    circuit.append(cirq.measure(qubits[2], qubits[1], qubits[0], key="meas"))

    simulator = cirq.Simulator(seed=42)
    result = simulator.run(circuit, repetitions=4096)

    measurements = result.measurements["meas"]
    counts = Counter("".join(str(int(bit)) for bit in row) for row in measurements)
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
