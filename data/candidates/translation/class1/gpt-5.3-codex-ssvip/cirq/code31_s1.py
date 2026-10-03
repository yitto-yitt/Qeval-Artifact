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
    repetitions = 1000
    result = simulator.run(circuit, repetitions=repetitions)
    histogram = result.multi_measurement_histogram(keys=["meas"])

    probs: Dict[str, float] = {}
    total = sum(histogram.values())
    for bits_tuple, count in histogram.items():
        bitstring = "".join(str(b) for b in bits_tuple)
        probs[bitstring] = count / total
    return probs
