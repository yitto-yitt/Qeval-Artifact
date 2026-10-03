# EVAL_META: task_id=28, framework=cirq, class=1
import cirq

def visualize_bell_states():
    q = [cirq.LineQubit(0), cirq.LineQubit(1)]

    phi_plus = cirq.Circuit()
    phi_plus.append(cirq.H(q[0]))
    phi_plus.append(cirq.CNOT(q[0], q[1]))
    phi_plus.append(cirq.measure(*q, key='meas'))

    phi_minus = cirq.Circuit()
    phi_minus.append(cirq.X(q[0]))
    phi_minus.append(cirq.H(q[0]))
    phi_minus.append(cirq.CNOT(q[0], q[1]))
    phi_minus.append(cirq.measure(*q, key='meas'))

    sim = cirq.Simulator()
    shots = 1000

    def get_counts(circuit):
        result = sim.run(circuit, repetitions=shots)
        meas = result.measurements['meas']
        counts = {}
        for row in meas:
            bitstring = ''.join(str(int(b)) for b in row)
            counts[bitstring] = counts.get(bitstring, 0) + 1
        return counts

    phi_plus_counts = get_counts(phi_plus)
    phi_minus_counts = get_counts(phi_minus)
    phi_plus_total = sum(phi_plus_counts.values())
    phi_minus_total = sum(phi_minus_counts.values())

    return {
        "phi_plus": {key: value / phi_plus_total for key, value in phi_plus_counts.items()},
        "phi_minus": {key: value / phi_minus_total for key, value in phi_minus_counts.items()},
    }
