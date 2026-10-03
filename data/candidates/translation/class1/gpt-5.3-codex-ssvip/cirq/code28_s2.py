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

    def probs_from_result(result):
        counts = result.multi_measurement_histogram(keys=["m"])
        total = sum(counts.values())
        dist = {}
        for bits_tuple, count in counts.items():
            bits = bits_tuple[0]
            bitstring = f"{bits[1]}{bits[0]}"
            dist[bitstring] = count / total
        return dist

    return {
        "phi_plus": probs_from_result(result_phi_plus),
        "phi_minus": probs_from_result(result_phi_minus),
    }
