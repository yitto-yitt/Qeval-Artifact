# EVAL_META: task_id=15, framework=cirq, class=1
import cirq
import numpy as np

def noisy_bell():
    # Create a Bell circuit in Cirq
    qubits = [cirq.LineQubit(i) for i in range(2)]
    circuit = cirq.Circuit()
    circuit.append(cirq.H(qubits[0]))
    circuit.append(cirq.CNOT(qubits[0], qubits[1]))
    circuit.append(cirq.measure(*qubits, key='meas'))
    
    # Simulate with noise (equivalent to noisy backend simulation)
    # Using depolarizing noise channel to simulate realistic noise
    noise_model = cirq.depolarize(p=0.01)
    noisy_circuit = cirq.Circuit(noise_model.on_each(*circuit.all_qubits()))
    noisy_circuit += circuit
    
    # Run the simulation
    simulator = cirq.DensityMatrixSimulator()
    result = simulator.run(noisy_circuit, repetitions=1000)
    
    # Get the measurement results
    measurements = result.measurements['meas']
    
    # Count the occurrences of each bitstring
    counts = {}
    for meas in measurements:
        bitstring = ''.join(map(str, meas))
        counts[bitstring] = counts.get(bitstring, 0) + 1
    
    # Convert to probability distribution
    total = sum(counts.values())
    prob_dist = {key: value / total for key, value in counts.items()}
    
    return prob_dist
