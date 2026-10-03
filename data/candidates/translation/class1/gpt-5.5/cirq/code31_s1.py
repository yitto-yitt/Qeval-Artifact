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

    counts: Dict[str, int] = {}
    for bits in result.measurements["meas"]:
        key = "".join(str(int(bit)) for bit in bits)
        counts[key] = counts.get(key, 0) + 1

    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
