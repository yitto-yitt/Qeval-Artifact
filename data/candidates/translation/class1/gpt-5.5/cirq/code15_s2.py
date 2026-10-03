# EVAL_META: task_id=15, framework=cirq, class=1
import cirq
from collections import Counter

def noisy_bell():
    q0, q1 = cirq.LineQubit.range(2)

    bell = cirq.Circuit()
    bell.append(cirq.H(q0))
    bell.append(cirq.CNOT(q0, q1))

    depol_p = 0.003
    readout_p = 0.02

    noisy_circuit = cirq.Circuit()
    noisy_circuit.append(cirq.H(q0))
    noisy_circuit.append(cirq.depolarize(depol_p).on_each(q0, q1))
    noisy_circuit.append(cirq.CNOT(q0, q1))
    noisy_circuit.append(cirq.depolarize(depol_p).on_each(q0, q1))
    noisy_circuit.append(cirq.bit_flip(readout_p).on_each(q0, q1))
    noisy_circuit.append(cirq.measure(q0, q1, key="meas"))

    simulator = cirq.DensityMatrixSimulator(seed=12345)
    result = simulator.run(noisy_circuit, repetitions=1000)

    counts = Counter()
    for row in result.measurements["meas"]:
        bitstring = "".join(str(int(bit)) for bit in row[::-1])
        counts[bitstring] += 1

    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
