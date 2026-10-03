# EVAL_META: task_id=40, framework=cirq, class=1
import cirq
import numpy as np

def init_random_3qubit(desired_vector):
    qubits = [cirq.LineQubit(i) for i in range(3)]
    circuit = cirq.Circuit()
    
    # Prepare the initial state using the desired vector
    psi = cirq.StateVectorTrialResult(
        params=cirq.ParamResolver({}),
        final_simulator_state=cirq.StateVectorSimulationState(
            initial_state=desired_vector,
            qubits=qubits
        )
    )
    
    # Add measurement gates
    circuit.append(cirq.measure(*qubits, key='result'))
    
    # Simulate the circuit
    simulator = cirq.Simulator(seed=42)
    result = simulator.run(circuit, repetitions=10000)  # Run multiple shots to get probabilities
    
    # Count the results
    measurements = result.measurements['result']
    counts = {}
    for meas in measurements:
        bitstring = ''.join(map(str, meas))
        counts[bitstring] = counts.get(bitstring, 0) + 1
    
    # Convert counts to probabilities
    total = sum(counts.values())
    prob_dist = {key: value / total for key, value in counts.items()}
    
    return prob_dist
