# EVAL_META: task_id=28, framework=cirq, class=1
import cirq

def visualize_bell_states():
    q0, q1 = cirq.LineQubit.range(2)
    phi_plus = cirq.Circuit(cirq.H(q0), cirq.CNOT(q0, q1), cirq.measure(q0, q1, key='meas'))
    phi_minus = cirq.Circuit(cirq.X(q0), cirq.H(q0), cirq.CNOT(q0, q1), cirq.measure(q0, q1, key='meas'))
    simulator = cirq.Simulator()
    result_plus = simulator.run(phi_plus, repetitions=1000)
    result_minus = simulator.run(phi_minus, repetitions=1000)
    counts_plus = result_plus.histogram(key='meas')
    counts_minus = result_minus.histogram(key='meas')
    phi_plus_probs = {format(k, '02b'): v / 1000 for k, v in counts_plus.items()}
    phi_minus_probs = {format(k, '02b'): v / 1000 for k, v in counts_minus.items()}
    return {
        "phi_plus": phi_plus_probs,
        "phi_minus": phi_minus_probs,
    }
