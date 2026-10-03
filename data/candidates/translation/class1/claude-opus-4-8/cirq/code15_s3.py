# EVAL_META: task_id=15, framework=cirq, class=1
import cirq

def noisy_bell():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit()
    circuit.append(cirq.H(q0))
    circuit.append(cirq.CNOT(q0, q1))
    noise_model = cirq.ConstantQubitNoiseModel(cirq.depolarize(0.02))
    noisy_circuit = circuit.with_noise(noise_model)
    noisy_circuit.append(cirq.measure(q0, q1, key='meas'))
    simulator = cirq.Simulator()
    result = simulator.run(noisy_circuit, repetitions=1000)
    counts = result.histogram(key='meas')
    total = sum(counts.values())
    dist = {}
    for value, count in counts.items():
        bitstring = format(value, '02b')
        dist[bitstring] = count / total
    return dist
