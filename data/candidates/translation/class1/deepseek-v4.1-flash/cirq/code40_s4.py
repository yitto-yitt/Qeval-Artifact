# EVAL_META: task_id=40, framework=cirq, class=1
import cirq
import numpy as np

def init_random_3qubit(desired_vector):
    qubits = cirq.LineQubit.range(3)
    state = np.array(desired_vector, dtype=complex)
    state = state / np.linalg.norm(state)
    circuit = cirq.Circuit(
        cirq.StatePreparationChannel(state).on(*qubits),
        cirq.measure(*qubits, key='m')
    )
    simulator = cirq.DensityMatrixSimulator()
    result = simulator.run(circuit, repetitions=100000)
    counts = result.histogram(key='m')
    total = sum(counts.values())
    dist = {}
    for bits, count in counts.items():
        bitstring = ''.join(str(bits[i]) for i in [2, 1, 0])
        dist[bitstring] = count / total
    return dist
