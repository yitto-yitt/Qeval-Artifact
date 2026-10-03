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

    phi_plus_hist = result_phi_plus.multi_measurement_histogram(keys=["m"])
    phi_minus_hist = result_phi_minus.multi_measurement_histogram(keys=["m"])

    phi_plus_counts = {}
    for k, v in phi_plus_hist.items():
        bits = k[0]
        bitstring = f"{bits[1]}{bits[0]}"
        phi_plus_counts[bitstring] = phi_plus_counts.get(bitstring, 0) + v

    phi_minus_counts = {}
    for k, v in phi_minus_hist.items():
        bits = k[0]
        bitstring = f"{bits[1]}{bits[0]}"
        phi_minus_counts[bitstring] = phi_minus_counts.get(bitstring, 0) + v

    phi_plus_total = sum(phi_plus_counts.values())
    phi_minus_total = sum(phi_minus_counts.values())

    return {
        "phi_plus": {key: value / phi_plus_total for key, value in phi_plus_counts.items()},
        "phi_minus": {key: value / phi_minus_total for key, value in phi_minus_counts.items()},
    }
