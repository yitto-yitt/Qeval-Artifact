# EVAL_META: task_id=31, framework=cirq, class=1
import cirq
from typing import Dict

def sampler_qiskit() -> Dict[str, float]:
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key='m')
    )
    
    simulator = cirq.Simulator(seed=42)
    result = simulator.run(circuit, repetitions=4000)
    
    measurements = result.measurements['m']
    counts = {}
    for row in measurements:
        # Qiskit uses little-endian (q0 is the rightmost bit)
        # Cirq's measurement array has q0 at index 0, q1 at index 1
        # Reversing the row matches Qiskit's bitstring format
        bitstring = ''.join(str(int(x)) for x in reversed(row))
        counts[bitstring] = counts.get(bitstring, 0) + 1
        
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
