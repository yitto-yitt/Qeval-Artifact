# EVAL_META: task_id=15, framework=cirq, class=1
import cirq
import numpy as np


def noisy_bell():
    q0, q1 = cirq.LineQubit.range(2)

    circuit = cirq.Circuit(
        cirq.rz(np.pi / 2)(q0),
        cirq.X(q0) ** 0.5,
        cirq.depolarize(0.001)(q0),
        cirq.rz(np.pi / 2)(q0),
        cirq.CNOT(q0, q1),
        cirq.depolarize(0.015, n_qubits=2)(q0, q1),
        cirq.bit_flip(0.02)(q0),
        cirq.bit_flip(0.02)(q1),
        cirq.measure(q1, q0, key="meas"),
    )

    simulator = cirq.DensityMatrixSimulator()
    result = simulator.run(circuit, repetitions=1000)
    counts = result.histogram(key="meas")
    total = sum(counts.values())
    return {format(key, "02b"): value / total for key, value in counts.items()}
