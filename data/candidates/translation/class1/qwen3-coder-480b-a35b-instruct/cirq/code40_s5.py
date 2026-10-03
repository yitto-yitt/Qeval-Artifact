# EVAL_META: task_id=40, framework=cirq, class=1
import cirq
import numpy as np

def init_random_3qubit(desired_vector):
    qubits = [cirq.LineQubit(i) for i in range(3)]
    circuit = cirq.Circuit()
    
    # Prepare the initial state using the desired vector
    psi = cirq.StateVectorTrialResult(
        params=cirq.ParamResolver({}),
        final_simulator_state=cirq.ActOnStateVectorArgs(
            available_buffer=np.empty_like(desired_vector),
            initial_state_vector=desired_vector,
            qid_shape=(2, 2, 2)
        ).final_state_vector
    )
    
    # Add the state preparation to the circuit
    circuit.append(cirq.StatePreparationChannel(desired_vector).on(*qubits))
    
    # Add measurements
    circuit.append(cirq.measure(*qubits, key='meas'))
    
    # Simulate the circuit
    simulator = cirq.Simulator(seed=42)
    result = simulator.run(circuit, repetitions=10000)  # Using many repetitions to approximate probabilities
    
    # Count the results
    measurements = result.histogram(key='meas')
    total = sum(measurements.values())
    
    # Convert to probability distribution
    prob_dist = {}
    for bitstring_int, count in measurements.items():
        # Convert integer to 3-bit binary string
        bitstring = format(bitstring_int, '03b')
        prob_dist[bitstring] = count / total
    
    return prob_dist
