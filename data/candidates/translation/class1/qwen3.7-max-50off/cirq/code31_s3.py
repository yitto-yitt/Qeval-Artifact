# EVAL_META: task_id=31, framework=cirq, class=1
import cirq

def sampler_qiskit():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key='meas')
    )
    
    simulator = cirq.Simulator(seed=42)
    result = simulator.run(circuit, repetitions=1024)
    
    counts = {}
    for measurement in result.measurements['meas']:
        bitstring = ''.join(str(int(b)) for b in measurement[::-1])
        counts[bitstring] = counts.get(bitstring, 0) + 1
        
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
