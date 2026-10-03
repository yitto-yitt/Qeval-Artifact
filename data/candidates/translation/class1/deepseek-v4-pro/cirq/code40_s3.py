# EVAL_META: task_id=40, framework=cirq, class=1
import numpy as np
import cirq

def init_random_3qubit(desired_vector):
    qubits = cirq.LineQubit.range(3)
    circuit = cirq.Circuit()

    # Initialize state from desired_vector
    circuit.append(cirq.StatePreparationChannel(desired_vector).on(*qubits))

    # Measure all qubits
    circuit.append(cirq.measure(*qubits, key='meas'))

    # Simulate with fixed seed
    simulator = cirq.Simulator(seed=42)
    result = simulator.run(circuit, repetitions=1024)

    # Extract measurement histogram
    hist = result.histogram(key='meas')
    total = sum(hist.values())
    # Convert to bitstring keys
    return {format(k, '03b'): v / total for k, v in hist.items()}
