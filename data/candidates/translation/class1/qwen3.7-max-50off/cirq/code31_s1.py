# EVAL_META: task_id=31, framework=cirq, class=1
import cirq

def sampler_qiskit():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key='m')
    )
    
    simulator = cirq.Simulator(seed=42)
    result = simulator.run(circuit, repetitions=1024)
    
    counts = {}
    for row in result.measurements['m']:
        bitstring = f"{row[1]}{row[0]}"
        counts[bitstring] = counts.get(bitstring, 0) + 1
        
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
