# EVAL_META: task_id=15, framework=cirq, class=1
import cirq

def noisy_bell():
    q0, q1 = cirq.LineQubit(0), cirq.LineQubit(1)
    circuit = cirq.Circuit()
    circuit.append(cirq.H(q0))
    circuit.append(cirq.CNOT(q0, q1))
    circuit.append(cirq.measure(q0, q1, key='m'))
    
    # Transpile the circuit to a target gateset (CZ gateset)
    compiled_circuit = cirq.optimize_for_target_gateset(circuit, gateset=cirq.CZTargetGateset())
    
    # Apply depolarizing noise to simulate a noisy device
    noisy_circuit = compiled_circuit.with_noise(cirq.depolarize(p=0.02))
    
    # Run the simulation
    simulator = cirq.Simulator()
    result = simulator.run(noisy_circuit, repetitions=1000)
    
    # Process results to match Qiskit's little-endian bitstring format
    measurements = result.measurements['m']
    counts = {}
    for row in measurements:
        bitstring = "".join(str(b) for b in reversed(row))
        counts[bitstring] = counts.get(bitstring, 0) + 1
        
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
