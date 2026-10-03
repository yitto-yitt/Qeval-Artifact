# EVAL_META: task_id=15, framework=cirq, class=1
import cirq


def noisy_bell():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key="meas"),
    )

    noise_model = cirq.NoiseModel.from_noise_model_like(cirq.depolarize(p=0.01))
    noisy_circuit = circuit.with_noise(noise_model)

    optimized_circuit = cirq.optimize_for_target_gateset(
        noisy_circuit, gateset=cirq.CZTargetGateset()
    )

    simulator = cirq.DensityMatrixSimulator()
    result = simulator.run(optimized_circuit, repetitions=1000)
    histogram = result.multi_measurement_histogram(keys=["meas"])

    total = sum(histogram.values())
    probs = {}
    for bits_tuple, count in histogram.items():
        bitstring = "".join(str(b) for b in bits_tuple)
        probs[bitstring] = count / total
    return probs
