# EVAL_META: task_id=28, framework=cirq, class=1
import cirq

def visualize_bell_states():
    q0 = cirq.LineQubit(0)
    q1 = cirq.LineQubit(1)

    # phi+ Bell state: (|00⟩ + |11⟩)/√2
    phi_plus_circuit = cirq.Circuit(
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q1, q0, key='result')  # reverse order to match Qiskit bitstring ordering
    )

    # phi- Bell state: (|00⟩ - |11⟩)/√2
    phi_minus_circuit = cirq.Circuit(
        cirq.X(q0),
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q1, q0, key='result')
    )

    simulator = cirq.Simulator()
    result_plus = simulator.run(phi_plus_circuit, repetitions=1000)
    result_minus = simulator.run(phi_minus_circuit, repetitions=1000)

    plus_counts = result_plus.histogram(key='result')
    minus_counts = result_minus.histogram(key='result')

    plus_total = sum(plus_counts.values())
    minus_total = sum(minus_counts.values())

    phi_plus_probs = {f'{v:02b}': plus_counts[v] / plus_total for v in plus_counts}
    phi_minus_probs = {f'{v:02b}': minus_counts[v] / minus_total for v in minus_counts}

    return {
        'phi_plus': phi_plus_probs,
        'phi_minus': phi_minus_probs
    }
