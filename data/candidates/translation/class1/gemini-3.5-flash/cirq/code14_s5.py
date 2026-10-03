# EVAL_META: task_id=14, framework=cirq, class=1
import cirq

def bell_each_shot():
    # Create qubits
    q0, q1 = cirq.LineQubit.range(2)
    
    # Create circuit
    circuit = cirq.Circuit(
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key='meas')
    )
    
    # Simulate the circuit for 10 shots
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=10)
    
    # Extract counts and convert to probability distribution
    measurements = result.measurements['meas']
    counts = {}
    for row in measurements:
        bitstring = "".join(str(x) for x in row)
        counts[bitstring] = counts.get(bitstring, 0) + 1
        
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
