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

    sim = cirq.Simulator()
    shots = 1000

    def counts(circuit):
        result = sim.run(circuit, repetitions=shots)
        meas = result.measurements['meas']
        c = {}
        for row in meas:
            bitstring = ''.join(str(int(b)) for b in row)
            c[bitstring] = c.get(bitstring, 0) + 1
        return c

    phi_plus_counts = counts(phi_plus)
    phi_minus_counts = counts(phi_minus)
    phi_plus_total = sum(phi_plus_counts.values())
    phi_minus_total = sum(phi_minus_counts.values())

    return {
        "phi_plus": {key: value / phi_plus_total for key, value in phi_plus_counts.items()},
        "phi_minus": {key: value / phi_minus_total for key, value in phi_minus_counts.items()},
    }
