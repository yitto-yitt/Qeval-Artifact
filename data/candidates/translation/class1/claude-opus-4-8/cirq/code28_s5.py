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

    def run(circuit):
        result = sim.run(circuit, repetitions=shots)
        arr = result.measurements['meas']
        counts = {}
        for row in arr:
            bits = ''.join(str(int(b)) for b in row[::-1])
            counts[bits] = counts.get(bits, 0) + 1
        total = sum(counts.values())
        return {k: v / total for k, v in counts.items()}

    return {
        "phi_plus": run(phi_plus),
        "phi_minus": run(phi_minus),
    }
