# EVAL_META: task_id=40, framework=cirq, class=1
import numpy as np
import cirq

def init_random_3qubit(desired_vector):
    qubits = cirq.LineQubit.range(3)
    state = np.asarray(desired_vector, dtype=np.complex128)
    norm = np.linalg.norm(state)
    if norm == 0:
        raise ValueError("desired_vector must be non-zero.")
    state = state / norm

    circuit = cirq.Circuit()
    circuit.append(cirq.StatePreparationChannel(state).on(*qubits))
    circuit.append(cirq.measure(*qubits, key="meas"))

    simulator = cirq.Simulator(seed=42)
    repetitions = 1024
    result = simulator.run(circuit, repetitions=repetitions)
    histogram = result.multi_measurement_histogram(keys=["meas"])

    probs = {}
    for key_tuple, count in histogram.items():
        bits = key_tuple[0]
        bitstring = "".join(str(int(b)) for b in bits[::-1])
        probs[bitstring] = count / repetitions
    return probs
