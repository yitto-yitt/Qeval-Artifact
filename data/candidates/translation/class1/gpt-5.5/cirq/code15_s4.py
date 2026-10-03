# EVAL_META: task_id=15, framework=cirq, class=1
import cirq


def noisy_bell():
    q0, q1 = cirq.LineQubit.range(2)

    circuit = cirq.Circuit(
        cirq.H(q0),
        cirq.depolarize(0.001).on(q0),
        cirq.CNOT(q0, q1),
        cirq.depolarize(0.01).on(q0),
        cirq.depolarize(0.01).on(q1),
        cirq.measure(q0, q1, key="meas"),
    )

    simulator = cirq.DensityMatrixSimulator()
    result = simulator.run(circuit, repetitions=1000)

    counts = result.histogram(
        key="meas",
        fold_func=lambda bits: "".join(str(int(bit)) for bit in bits),
    )
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
