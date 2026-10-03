# EVAL_META: task_id=40, framework=cirq, class=1
import cirq
import numpy as np

def init_random_3qubit(desired_vector):
    qubits = cirq.LineQubit.range(3)
    circuit = cirq.Circuit()
    
    # In Cirq, StatePreparationChannel can be used to initialize a state.
    # It takes a target state vector and prepares it.
    prep = cirq.StatePreparationChannel(target_state=np.array(desired_vector, dtype=np.complex128))
    circuit.append(prep.on(*qubits))
    circuit.append(cirq.measure(*qubits, key='meas'))
    
    # Simulate the circuit. Since it uses a StatePreparationChannel,
    # we can use the density matrix simulator or standard simulator.
    # We set a seed of 42 to match the Qiskit reference's seed_simulator=42 behavior.
    simulator = cirq.Simulator(seed=42)
    result = simulator.run(circuit, repetitions=1024)
    
    # Get counts and convert to a probability distribution dictionary
    counts = result.histogram(key='meas')
    total = sum(counts.values())
    
    # Convert keys to binary strings matching the Qiskit representation (3 bits)
    prob_dist = {}
    for state_int, count in counts.items():
        bitstring = f"{state_int:03b}"
        prob_dist[bitstring] = count / total
        
    return prob_dist
