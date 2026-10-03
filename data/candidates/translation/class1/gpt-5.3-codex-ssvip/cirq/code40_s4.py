# EVAL_META: task_id=40, framework=cirq, class=1
import cirq
import numpy as np

def init_random_3qubit(desired_vector):
    q0, q1, q2 = cirq.LineQubit.range(3)
    qubits = [q0, q1, q2]

    state = np.asarray(desired_vector, dtype=np.complex128)
    state = state / np.linalg.norm(state)

    circuit = cirq.Circuit()
    circuit.append(cirq.StatePreparationChannel(state).on(*qubits))
    circuit.append(cirq.measure(*qubits, key="meas"))

    simulator = cirq.Simulator(seed=42)
    repetitions = 1000
    result = simulator.run(circuit, repetitions=repetitions)

    hist = result.multi_measurement_histogram(keys=["meas"])
    probs = {}
    for key_tuple, count in hist.items():
        bits = key_tuple[0]
        bitstring = "".join(str(int(b)) for b in bits[::-1])
        probs[bitstring] = count / repetitions
    return probs
