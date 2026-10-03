# EVAL_META: task_id=31, framework=cirq, class=1
from typing import Dict
import cirq


def sampler_qiskit():
    q = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(
        cirq.H(q[0]),
        cirq.CNOT(q[0], q[1]),
        cirq.measure(q[0], q[1], key="meas"),
    )

    simulator = cirq.Simulator(seed=42)
    result = simulator.run(circuit, repetitions=4096)

    counts = result.histogram(key="meas")
    total = sum(counts.values())
    return {format(key, "02b"): value / total for key, value in counts.items()}
