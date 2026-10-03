# EVAL_META: task_id=28, framework=cirq, class=1
import cirq

def visualize_bell_states():
    # Qubits
    q0, q1 = cirq.LineQubit.range(2)

    # Phi+ circuit: H(0), CNOT(0,1)
    phi_plus_circuit = cirq.Circuit([
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key='result')
    ])

    # Phi- circuit: X(0), H(0), CNOT(0,1)
    phi_minus_circuit = cirq.Circuit([
        cirq.X(q0),
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key='result')
    ])

    # Simulate
    simulator = cirq.Simulator()
    shots = 1000

    result_phi_plus = simulator.run(phi_plus_circuit, repetitions=shots)
    result_phi_minus = simulator.run(phi_minus_circuit, repetitions=shots)

    # Extract counts
    phi_plus_counts = result_phi_plus.histogram(key='result')
    phi_minus_counts = result_phi_minus.histogram(key='result')

    # Convert to bitstring keys and normalize to probabilities
    phi_plus_dist = {format(k, '02b'): v / shots for k, v in phi_plus_counts.items()}
    phi_minus_dist = {format(k, '02b'): v / shots for k, v in phi_minus_counts.items()}

    return {
        "phi_plus": phi_plus_dist,
        "phi_minus": phi_minus_dist,
    }
