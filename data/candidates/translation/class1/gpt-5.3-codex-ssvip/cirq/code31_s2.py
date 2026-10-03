# EVAL_META: task_id=31, framework=cirq, class=1
from typing import Dict
import cirq


def sampler_qiskit():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key="meas"),
    )
    simulator = cirq.Simulator(seed=42)
    result = simulator.run(circuit, repetitions=1000)
    histogram = result.multi_measurement_histogram(keys=["meas"])
    total = sum(histogram.values())
    probs: Dict[str, float] = {}
    for bits, count in histogram.items():
        bitstring = "".join(str(b) for b in bits[::-1])
        probs[bitstring] = count / total
    return probs
