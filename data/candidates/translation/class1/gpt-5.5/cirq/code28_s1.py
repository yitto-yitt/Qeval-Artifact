# EVAL_META: task_id=28, framework=cirq, class=1
import cirq
from collections import Counter

def visualize_bell_states():
    q0, q1 = cirq.LineQubit.range(2)

    phi_plus = cirq.Circuit(
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key="meas"),
    )

    phi_minus = cirq.Circuit(
        cirq.X(q0),
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key="meas"),
    )

    simulator = cirq.Simulator()
    result_phi_plus = simulator.run(phi_plus, repetitions=1000)
    result_phi_minus = simulator.run(phi_minus, repetitions=1000)

    def probabilities(result):
        measurements = result.measurements["meas"]
        counts = Counter("".join(str(int(bit)) for bit in row) for row in measurements)
        total = sum(counts.values())
        return {key: value / total for key, value in counts.items()}

    return {
        "phi_plus": probabilities(result_phi_plus),
        "phi_minus": probabilities(result_phi_minus),
    }
