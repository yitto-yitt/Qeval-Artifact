# EVAL_META: task_id=28, framework=cirq, class=1
import cirq

def visualize_bell_states():
    # Define two qubits
    q0, q1 = cirq.LineQubit.range(2)

    # Build phi_plus circuit: H on q0, then CNOT q0->q1
    phi_plus_circuit = cirq.Circuit([
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key='meas')
    ])

    # Build phi_minus circuit: X on q0, H on q0, then CNOT q0->q1
    phi_minus_circuit = cirq.Circuit([
        cirq.X(q0),
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key='meas')
    ])

    # Simulate both circuits
    simulator = cirq.Simulator()
    shots = 1000

    result_phi_plus = simulator.run(phi_plus_circuit, repetitions=shots)
    result_phi_minus = simulator.run(phi_minus_circuit, repetitions=shots)

    # Extract measurement counts
    phi_plus_counts = result_phi_plus.histogram(key='meas')
    phi_minus_counts = result_phi_minus.histogram(key='meas')

    # Convert integer keys to bitstrings (e.g., 0 -> '00', 3 -> '11')
    phi_plus_dict = {format(k, '02b'): v for k, v in phi_plus_counts.items()}
    phi_minus_dict = {format(k, '02b'): v for k, v in phi_minus_counts.items()}

    # Normalize to probabilities
    phi_plus_total = sum(phi_plus_dict.values())
    phi_minus_total = sum(phi_minus_dict.values())

    return {
        "phi_plus": {key: value / phi_plus_total for key, value in phi_plus_dict.items()},
        "phi_minus": {key: value / phi_minus_total for key, value in phi_minus_dict.items()},
    }
