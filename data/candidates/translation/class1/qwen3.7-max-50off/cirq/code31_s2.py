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
    result = simulator.run(circuit, repetitions=1024)
    
    measurements = result.measurements['m']
    counts = {}
    for row in measurements:
        bs = f"{row[1]}{row[0]}"
        counts[bs] = counts.get(bs, 0) + 1
        
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
