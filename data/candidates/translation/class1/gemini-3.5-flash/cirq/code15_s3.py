# EVAL_META: task_id=15, framework=cirq, class=1
import cirq

def noisy_bell():
    q0 = cirq.LineQubit(0)
    q1 = cirq.LineQubit(1)
    
    circuit = cirq.Circuit(
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q1, q0, key='meas')
    )
    
    # Simulate a noisy environment using depolarizing noise
    noisy_circuit = circuit.with_noise(cirq.depolarize(0.02))
    
    simulator = cirq.Simulator()
    result = simulator.run(noisy_circuit, repetitions=1000)
    
    counts = {}
    for row in result.measurements['meas']:
        bitstring = ''.join(str(x) for x in row)
        counts[bitstring] = counts.get(bitstring, 0) + 1
        
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
