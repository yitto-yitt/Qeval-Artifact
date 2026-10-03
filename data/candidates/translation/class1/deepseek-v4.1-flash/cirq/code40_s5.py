# EVAL_META: task_id=40, framework=cirq, class=1
import cirq
import numpy as np

def init_random_3qubit(desired_vector):
    qubits = cirq.LineQubit.range(3)
    desired_vector = np.asarray(desired_vector, dtype=complex)
    rev_vector = np.zeros(8, dtype=complex)
    for i in range(8):
        rev_i = int(format(i, '03b')[::-1], 2)
        rev_vector[i] = desired_vector[rev_i]
    circuit = cirq.Circuit()
    circuit.append(cirq.StatePreparationChannel(rev_vector).on(*qubits))
    circuit.append(cirq.measure(*qubits[::-1], key='m'))
    simulator = cirq.Simulator(seed=42)
    result = simulator.run(circuit, repetitions=1024)
    counts = result.histogram(key='m')
    total = sum(counts.values())
    return {format(k, '03b'): v / total for k, v in counts.items()}
