# EVAL_META: task_id=1, framework=cirq, class=1
import cirq

def run_bell_state_simulator():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit()
    circuit.append(cirq.H(q0))
    circuit.append(cirq.CNOT(q0, q1))
    circuit.append(cirq.measure(q0, q1, key='meas'))
    simulator = cirq.Simulator()
    shots = 1000
    result = simulator.run(circuit, repetitions=shots)
    measurements = result.measurements['meas']
    counts = {}
    for shot in measurements:
        key = ''.join(str(int(b)) for b in shot)
        counts[key] = counts.get(key, 0) + 1
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
