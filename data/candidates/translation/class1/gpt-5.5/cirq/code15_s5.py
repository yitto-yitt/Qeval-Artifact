# EVAL_META: task_id=15, framework=cirq, class=1
import cirq


def noisy_bell():
    q0, q1 = cirq.LineQubit.range(2)

    circuit = cirq.Circuit(
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key="meas"),
    )

    noise = cirq.depolarize(p=0.001)
    simulator = cirq.DensityMatrixSimulator(noise=noise)

    result = simulator.run(circuit, repetitions=1000)
    measurements = result.measurements["meas"]

    counts = {}
    for row in measurements:
        bitstring = "".join(str(int(bit)) for bit in row[::-1])
        counts[bitstring] = counts.get(bitstring, 0) + 1

    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
