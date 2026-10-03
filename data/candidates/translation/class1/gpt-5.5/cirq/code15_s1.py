# EVAL_META: task_id=15, framework=cirq, class=1
import cirq


def noisy_bell():
    q0, q1 = cirq.LineQubit.range(2)

    bell = cirq.Circuit()
    bell.append(cirq.H(q0))
    bell.append(cirq.CNOT(q0, q1))
    bell.append(cirq.measure(q0, q1, key="meas"))

    optimized = cirq.optimize_for_target_gateset(bell, gateset=cirq.CZTargetGateset())

    noise = cirq.NoiseModel.from_noise_model_like(cirq.depolarize(p=0.003))
    simulator = cirq.Simulator(noise=noise)

    result = simulator.run(optimized, repetitions=1000)
    measurements = result.measurements["meas"]

    counts = {}
    for row in measurements:
        bitstring = "".join(str(int(bit)) for bit in row)
        counts[bitstring] = counts.get(bitstring, 0) + 1

    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
