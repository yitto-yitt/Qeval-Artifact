# EVAL_META: task_id=31, framework=cirq, class=1
import cirq
from typing import Dict

def sampler_qiskit():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key='result')
    )
    sim = cirq.Simulator(seed=42)
    result = sim.run(circuit, repetitions=1024)
    counts = result.histogram(key='result')
    total = sum(counts.values())
    return {format(k, '02b'): v / total for k, v in counts.items()}
