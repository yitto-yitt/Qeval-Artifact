# EVAL_META: task_id=28, framework=cirq, class=1
import cirq


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

    def run_and_probs(circuit):
        result = simulator.run(circuit, repetitions=1000)
        counts = result.histogram(key="meas")
        total = sum(counts.values())
        return {format(key, "02b"): value / total for key, value in counts.items()}

    return {
        "phi_plus": run_and_probs(phi_plus),
        "phi_minus": run_and_probs(phi_minus),
    }
