# EVAL_META: task_id=14, framework=cirq, class=1
import cirq

def bell_each_shot():
    # Create qubits
    q0, q1 = cirq.LineQubit.range(2)

    # Build the Bell circuit
    circuit = cirq.Circuit([
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key='result'),
    ])

    # Simulate with 10 shots
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=10)

    # Extract measurement outcomes
    counts = result.histogram(key='result')

    # Convert to probability distribution
    total = sum(counts.values())
    return {format(k, '02b'): v / total for k, v in counts.items()}
