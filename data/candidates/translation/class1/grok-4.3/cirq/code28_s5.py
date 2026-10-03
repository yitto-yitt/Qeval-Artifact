# EVAL_META: task_id=28, framework=cirq, class=1
import cirq

def visualize_bell_states():
    q0, q1 = cirq.LineQubit.range(2)
    phi_plus = cirq.Circuit(
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key='meas')
    )
    phi_minus = cirq.Circuit(
        cirq.X(q0),
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key='meas')
    )
    simulator = cirq.Simulator()
    result_phi_plus = simulator.run(phi_plus, repetitions=1000)
    result_phi_minus = simulator.run(phi_minus, repetitions=1000)
    counts_plus = result_phi_plus.histogram(key='meas')
    counts_minus = result_phi_minus.histogram(key='meas')
    total_plus = sum(counts_plus.values())
    total_minus = sum(counts_minus.values())
    return {
        "phi_plus": {format(k, '02b'): v / total_plus for k, v in counts_plus.items()},
        "phi_minus": {format(k, '02b'): v / total_minus for k, v in counts_minus.items()},
    }
