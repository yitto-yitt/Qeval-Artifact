# EVAL_META: task_id=15, framework=cirq, class=1
import cirq

def noisy_bell():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit()
    circuit.append(cirq.H(q0))
    circuit.append(cirq.CNOT(q0, q1))

    p = 0.02
    circuit.append(cirq.depolarize(p).on(q0))
    circuit.append(cirq.depolarize(p).on(q1))

    circuit.append(cirq.measure(q0, q1, key='meas'))

    simulator = cirq.DensityMatrixSimulator()
    shots = 1000
    result = simulator.run(circuit, repetitions=shots)

    measurements = result.measurements['meas']
    counts = {}
    for shot in measurements:
        bitstring = ''.join(str(int(b)) for b in shot)
        counts[bitstring] = counts.get(bitstring, 0) + 1

    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
