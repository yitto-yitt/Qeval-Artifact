# EVAL_META: task_id=40, framework=cirq, class=1
import cirq
import numpy as np

def init_random_3qubit(desired_vector):
    qubits = cirq.LineQubit.range(3)
    circuit = cirq.Circuit(cirq.measure(qubits[2], qubits[1], qubits[0], key='meas'))
    simulator = cirq.Simulator(seed=42)
    result = simulator.run(circuit, initial_state=np.asarray(desired_vector, dtype=complex), repetitions=1024)
    counts = result.histogram(key='meas')
    total = sum(counts.values())
    return {f"{key:03b}": value / total for key, value in counts.items()}
