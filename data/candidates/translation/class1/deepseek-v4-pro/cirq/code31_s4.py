# EVAL_META: task_id=31, framework=cirq, class=1
from typing import Dict
import cirq

def sampler_qiskit():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit([
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key='result'),
    ])

    simulator = cirq.Simulator(seed=42)
    result = simulator.run(circuit, repetitions=1024)
    counts = result.histogram(key='result')
    total = sum(counts.values())
    return {format(k, '02b'): v / total for k, v in counts.items()}
