# EVAL_META: task_id=40, framework=cirq, class=1
import cirq
import numpy as np

def init_random_3qubit(desired_vector):
    # Normalize the state vector as Qiskit's initialize does
    state_vector = np.array(desired_vector, dtype=complex)
    state_vector /= np.linalg.norm(state_vector)
    
    # Qiskit uses qubit order q0, q1, q2 with q0 as least significant bit.
    # Cirq uses big-endian ordering. To match Qiskit's statevector indexing,
    # we prepare and measure qubits in reverse order: q2, q1, q0.
    q0, q1, q2 = cirq.LineQubit.range(3)
    qubits = [q2, q1, q0]
    
    circuit = cirq.Circuit()
    circuit.append(cirq.StatePreparationChannel(state_vector).on(*qubits))
    circuit.append(cirq.measure(*qubits, key='m'))
    
    simulator = cirq.Simulator(seed=42)
    result = simulator.run(circuit, repetitions=1024)
    counts = result.histogram(key='m')
    total = sum(counts.values())
    
    prob_dist = {}
    for key, value in counts.items():
        bitstring = format(key, '03b')
        prob_dist[bitstring] = value / total
    return prob_dist
