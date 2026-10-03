# EVAL_META: task_id=40, framework=cirq, class=1
import numpy as np
import cirq


def init_random_3qubit(desired_vector):
    q0, q1, q2 = cirq.LineQubit.range(3)
    circuit = cirq.Circuit()
    circuit.append(cirq.StatePreparationChannel(np.asarray(desired_vector, dtype=np.complex128))(q0, q1, q2))
    circuit.append(cirq.measure(q0, q1, q2, key="meas"))
    simulator = cirq.Simulator(seed=42)
    repetitions = 1000
    result = simulator.run(circuit, repetitions=repetitions)
    hist = result.multi_measurement_histogram(keys=["meas"])
    probs = {}
    for bits, count in hist.items():
        bitstring = "".join(str(b) for b in bits)
        probs[bitstring] = count / repetitions
    return probs
