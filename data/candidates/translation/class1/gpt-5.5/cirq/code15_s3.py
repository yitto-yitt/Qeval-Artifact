# EVAL_META: task_id=15, framework=cirq, class=1
import cirq
from collections import Counter


def noisy_bell():
    q0, q1 = cirq.LineQubit.range(2)

    circuit = cirq.Circuit(
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key="meas"),
    )

    noise = cirq.NoiseModel.from_noise_model_like(cirq.depolarize(p=0.01))
    noisy_circuit = circuit.with_noise(noise)

    simulator = cirq.DensityMatrixSimulator()
    result = simulator.run(noisy_circuit, repetitions=1000)

    measurements = result.measurements["meas"]
    counts = Counter("".join(str(int(bit)) for bit in row) for row in measurements)
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
