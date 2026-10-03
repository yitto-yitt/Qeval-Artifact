# EVAL_META: task_id=28, framework=cirq, class=1
import cirq


def visualize_bell_states():
    q0, q1 = cirq.LineQubit.range(2)

    phi_plus_circuit = cirq.Circuit(
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key="m"),
    )

    phi_minus_circuit = cirq.Circuit(
        cirq.X(q0),
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key="m"),
    )

    simulator = cirq.Simulator()
    shots = 1000

    result_phi_plus = simulator.run(phi_plus_circuit, repetitions=shots)
    result_phi_minus = simulator.run(phi_minus_circuit, repetitions=shots)

    def counts_to_probs(result):
        counts = result.multi_measurement_histogram(keys=["m"])
        total = sum(counts.values())
        probs = {}
        for key, value in counts.items():
            bits = key[0]
            bitstring = "".join(str(int(b)) for b in bits[::-1])
            probs[bitstring] = value / total
        return probs

    return {
        "phi_plus": counts_to_probs(result_phi_plus),
        "phi_minus": counts_to_probs(result_phi_minus),
    }
