# EVAL_META: task_id=31, framework=cirq, class=1
from typing import Dict
from collections import Counter
import cirq

def sampler_qiskit() -> Dict[str, float]:
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key='m')
    )
    simulator = cirq.Simulator(seed=42)
    result = simulator.run(circuit, repetitions=1024)
    counts = Counter(''.join(str(int(bit)) for bit in row) for row in result.measurements['m'])
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
