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
    result = simulator.run(circuit, repetitions=4096)

    counts = result.histogram(key="meas", fold_func=cirq.big_endian_bits_to_int)
    total = sum(counts.values())
    return {format(key, "02b"): value / total for key, value in counts.items()}
