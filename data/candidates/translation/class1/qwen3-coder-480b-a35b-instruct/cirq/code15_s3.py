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
    noisy_circuit.append(circuit)
    
    # Run the simulation
    simulator = cirq.DensityMatrixSimulator()
    result = simulator.run(noisy_circuit, repetitions=1000)
    
    # Get measurement results and convert to bitstring counts
    measurements = result.measurements['meas']
    counts = {}
    for meas in measurements:
        bitstring = ''.join(map(str, meas[::-1]))  # Reverse order to match qiskit convention
        counts[bitstring] = counts.get(bitstring, 0) + 1
    
    # Normalize to get probabilities
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
