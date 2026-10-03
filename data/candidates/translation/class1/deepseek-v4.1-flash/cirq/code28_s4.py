# EVAL_META: task_id=28, framework=cirq, class=1
import cirq
from collections import Counter

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
    shots = 1000

    result_plus = simulator.run(phi_plus, repetitions=shots)
    result_minus = simulator.run(phi_minus, repetitions=shots)

    def probs_from_result(result):
        counts = Counter()
        for row in result.measurements['m']:
            bitstring = ''.join(str(int(b)) for b in row)
            counts[bitstring] += 1
        total = sum(counts.values())
        return {key: value / total for key, value in counts.items()}

    return {
        "phi_plus": probs_from_result(result_plus),
        "phi_minus": probs_from_result(result_minus),
    }
