# EVAL_META: task_id=28, framework=cirq, class=1
import cirq
import numpy as np

def visualize_bell_states():
    # Qubits
    q0, q1 = cirq.LineQubit.range(2)

    # Phi+ circuit: H(0), CNOT(0,1)
    phi_plus_circuit = cirq.Circuit([
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key='meas')
    ])

    # Phi- circuit: X(0), H(0), CNOT(0,1)
    phi_minus_circuit = cirq.Circuit([
        cirq.X(q0),
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key='meas')
    ])

    # Simulate
    simulator = cirq.Simulator()
    shots = 1000

    # Run Phi+
    result_phi_plus = simulator.run(phi_plus_circuit, repetitions=shots)
    counts_phi_plus = result_phi_plus.histogram(key='meas')
    phi_plus_total = shots
    phi_plus_dist = {format(k, '02b'): v / phi_plus_total for k, v in counts_phi_plus.items()}

    # Run Phi-
    result_phi_minus = simulator.run(phi_minus_circuit, repetitions=shots)
    counts_phi_minus = result_phi_minus.histogram(key='meas')
    phi_minus_total = shots
    phi_minus_dist = {format(k, '02b'): v / phi_minus_total for k, v in counts_phi_minus.items()}

    return {
        "phi_plus": phi_plus_dist,
        "phi_minus": phi_minus_dist,
    }
