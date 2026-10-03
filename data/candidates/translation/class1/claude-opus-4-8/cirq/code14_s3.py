# EVAL_META: task_id=14, framework=cirq, class=1
import cirq

def bell_each_shot():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit()
    circuit.append(cirq.H(q0))
    circuit.append(cirq.CNOT(q0, q1))
    circuit.append(cirq.measure(q0, q1, key='meas'))

    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=10)

    measurements = result.measurements['meas']
    counts = {}
    for shot in measurements:
        key = ''.join(str(int(b)) for b in shot)
        counts[key] = counts.get(key, 0) + 1

    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
