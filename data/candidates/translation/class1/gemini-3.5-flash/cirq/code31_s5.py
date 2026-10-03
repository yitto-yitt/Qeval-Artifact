# EVAL_META: task_id=31, framework=cirq, class=1
from typing import Dict
import cirq

def sampler_qiskit() -> Dict[str, float]:
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit()
    circuit.append(cirq.H(q0))
    circuit.append(cirq.CX(q0, q1))
    # Measure in order of q1, q0 to match Qiskit's MSB-first bitstring representation
    circuit.append(cirq.measure(q1, q0, key='m'))
    
    simulator = cirq.Simulator(seed=42)
    result = simulator.run(circuit, repetitions=1024)
    
    measurements = result.measurements['m']
    counts = {}
    for row in measurements:
        bitstring = "".join(str(bit) for bit in row)
        counts[bitstring] = counts.get(bitstring, 0) + 1
        
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
