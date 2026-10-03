# EVAL_META: task_id=28, framework=cirq, class=1
import cirq
import collections

def visualize_bell_states():
    q0, q1 = cirq.LineQubit.range(2)

    phi_plus = cirq.Circuit()
    phi_plus.append(cirq.H(q0))
    phi_plus.append(cirq.CNOT(q0, q1))
    phi_plus.append(cirq.measure(q0, q1, key='m'))

    phi_minus = cirq.Circuit()
    phi_minus.append(cirq.X(q0))
    phi_minus.append(cirq.H(q0))
    phi_minus.append(cirq.CNOT(q0, q1))
    phi_minus.append(cirq.measure(q0, q1, key='m'))

    simulator = cirq.Simulator()

    def get_probs(circuit):
        result = simulator.run(circuit, repetitions=1000)
        measurements = result.measurements['m']
        counts = collections.Counter()
        for row in measurements:
            # row[0] is q0, row[1] is q1; format as q1 q0 to match Qiskit bitstring order.
            bitstring = f"{int(row[1])}{int(row[0])}"
            counts[bitstring] += 1
        total = sum(counts.values())
        return {k: v / total for k, v in counts.items()}

    return {
        "phi_plus": get_probs(phi_plus),
        "phi_minus": get_probs(phi_minus),
    }
