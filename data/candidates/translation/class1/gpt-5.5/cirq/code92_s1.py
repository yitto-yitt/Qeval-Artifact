# EVAL_META: task_id=92, framework=cirq, class=1
import cirq
import numpy as np

def calculate_stabilizer_state_info():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit()
    circuit.append(cirq.H(q0))
    circuit.append(cirq.CNOT(q0, q1))

    simulator = cirq.Simulator()
    result = simulator.simulate(circuit, qubit_order=[q0, q1])
    state_vector = result.final_state_vector

    probabilities_dict = {}
    for i, amplitude in enumerate(state_vector):
        probability = float(np.abs(amplitude) ** 2)
        if probability > 1e-12:
            probabilities_dict[format(i, "02b")] = probability

    return probabilities_dict
