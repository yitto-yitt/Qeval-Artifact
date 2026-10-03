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

    def sample_probabilities(circuit):
        result = simulator.run(circuit, repetitions=1000)
        measurements = result.measurements["meas"]
        counts = {}
        for bits in measurements:
            bitstring = "".join(str(int(bit)) for bit in bits)
            counts[bitstring] = counts.get(bitstring, 0) + 1
        total = sum(counts.values())
        return {key: value / total for key, value in counts.items()}

    return {
        "phi_plus": sample_probabilities(phi_plus),
        "phi_minus": sample_probabilities(phi_minus),
    }
