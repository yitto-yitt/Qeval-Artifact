# EVAL_META: task_id=28, framework=cirq, class=1
import cirq

def visualize_bell_states():
    q0, q1 = cirq.LineQubit.range(2)

    phi_plus = cirq.Circuit([
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key='meas'),
    ])
    phi_minus = cirq.Circuit([
        cirq.X(q0),
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key='meas'),
    ])

    simulator = cirq.Simulator()
    shots = 1000

    def counts_to_dist(circuit):
        result = simulator.run(circuit, repetitions=shots)
        measurements = result.measurements['meas']
        counts = {}
        for row in measurements:
            bitstring = ''.join(str(int(b)) for b in row)
            counts[bitstring] = counts.get(bitstring, 0) + 1
        total = sum(counts.values())
        return {k: v / total for k, v in counts.items()}

    return {
        "phi_plus": counts_to_dist(phi_plus),
        "phi_minus": counts_to_dist(phi_minus),
    }
