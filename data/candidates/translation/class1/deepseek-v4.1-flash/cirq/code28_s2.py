# EVAL_META: task_id=28, framework=cirq, class=1
import cirq

def visualize_bell_states():
    q0, q1 = cirq.LineQubit.range(2)
    phi_plus = cirq.Circuit(
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key='m')
    )
    phi_minus = cirq.Circuit(
        cirq.X(q0),
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key='m')
    )

    simulator = cirq.Simulator(seed=1234)
    result_phi_plus = simulator.run(phi_plus, repetitions=1000)
    result_phi_minus = simulator.run(phi_minus, repetitions=1000)

    def counts_to_probs(result):
        measurements = result.measurements['m']
        counts = {}
        for row in measurements:
            bitstring = ''.join(str(int(bit)) for bit in row)
            counts[bitstring] = counts.get(bitstring, 0) + 1
        total = sum(counts.values())
        return {k: v / total for k, v in counts.items()}

    return {
        "phi_plus": counts_to_probs(result_phi_plus),
        "phi_minus": counts_to_probs(result_phi_minus),
    }
