# EVAL_META: task_id=40, framework=cirq, class=1
import cirq
import numpy as np

def init_random_3qubit(desired_vector):
    qubits = [cirq.LineQubit(i) for i in range(3)]
    state = np.asarray(desired_vector, dtype=np.complex128)
    state = state / np.linalg.norm(state)

    circuit = cirq.Circuit()
    circuit.append(cirq.StatePreparationChannel(state)(*qubits))
    circuit.append(cirq.measure(*qubits, key="meas"))

    simulator = cirq.Simulator(seed=42)
    repetitions = 1024
    result = simulator.run(circuit, repetitions=repetitions)
    hist = result.multi_measurement_histogram(keys=["meas"])

    probs = {}
    for key, count in hist.items():
        bits = key[0]
        bitstring = "".join(str(int(b)) for b in bits[::-1])
        probs[bitstring] = count / repetitions
    return probs
