# EVAL_META: task_id=28, framework=cirq, class=1
import cirq

def visualize_bell_states():
    q0, q1 = cirq.LineQubit.range(2)
    circuit_plus = cirq.Circuit(
        cirq.H(q0),
        cirq.CX(q0, q1),
        cirq.measure(q0, q1, key='result')
    )
    circuit_minus = cirq.Circuit(
        cirq.X(q0),
        cirq.H(q0),
        cirq.CX(q0, q1),
        cirq.measure(q0, q1, key='result')
    )
    simulator = cirq.Simulator()
    result_plus = simulator.run(circuit_plus, repetitions=1000)
    result_minus = simulator.run(circuit_minus, repetitions=1000)
    counts_plus = result_plus.histogram(key='result')
    counts_minus = result_minus.histogram(key='result')
    total_plus = sum(counts_plus.values())
    total_minus = sum(counts_minus.values())
    phi_plus_dist = {format(k, '02b'): v / total_plus for k, v in counts_plus.items()}
    phi_minus_dist = {format(k, '02b'): v / total_minus for k, v in counts_minus.items()}
    return {
        "phi_plus": phi_plus_dist,
        "phi_minus": phi_minus_dist,
    }
