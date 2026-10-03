# EVAL_META: task_id=1, framework=cirq, class=1
import cirq
import numpy as np

def run_bell_state_simulator():
    # Create a Bell state circuit (phi+ state: |00> + |11>)
    qubits = [cirq.LineQubit(0), cirq.LineQubit(1)]
    circuit = cirq.Circuit()
    circuit.append(cirq.H(qubits[0]))
    circuit.append(cirq.CNOT(qubits[0], qubits[1]))
    circuit.append(cirq.measure(qubits[0], qubits[1], key='meas'))
    
    # Simulate the circuit
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1000)
    
    # Get measurement results
    measurements = result.measurements['meas']
    
    # Count occurrences of each bitstring
    counts = {}
    for meas in measurements:
        bitstring = ''.join(map(str, meas))
        counts[bitstring] = counts.get(bitstring, 0) + 1
    
    # Convert to probability distribution
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
