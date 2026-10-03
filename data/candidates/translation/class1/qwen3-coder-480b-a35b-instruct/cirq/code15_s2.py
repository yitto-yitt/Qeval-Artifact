# EVAL_META: task_id=15, framework=cirq, class=1
import cirq
import numpy as np

def noisy_bell():
    # Create a Bell circuit in Cirq
    qubits = [cirq.LineQubit(0), cirq.LineQubit(1)]
    circuit = cirq.Circuit()
    circuit.append(cirq.H(qubits[0]))
    circuit.append(cirq.CNOT(qubits[0], qubits[1]))
    circuit.append(cirq.measure(*qubits, key='result'))
    
    # Simulate with noise (equivalent to noisy backend simulation)
    # Using depolarizing noise to simulate realistic device behavior
    noise_model = cirq.depolarize(p=0.01)  # Small noise rate
    noisy_circuit = cirq.Circuit(noise_model.on_each(*circuit.all_qubits()) if op.gate != cirq.MeasurementGate else op for op in circuit.all_operations())
    
    # Add noise operations properly
    noisy_circuit = cirq.Circuit()
    for moment in circuit:
        for op in moment:
            if isinstance(op.gate, (cirq.H, cirq.CNOT)):
                noisy_circuit.append([op, noise_model.on(*op.qubits)])
            else:
                noisy_circuit.append(op)
    
    # Simulate the circuit
    simulator = cirq.DensityMatrixSimulator()
    result = simulator.run(noisy_circuit, repetitions=1000)
    
    # Count results
    measurements = result.measurements['result']
    counts = {}
    for meas in measurements:
        bitstring = ''.join(map(str, meas[::-1]))  # Reverse order to match qiskit convention
        counts[bitstring] = counts.get(bitstring, 0) + 1
    
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
