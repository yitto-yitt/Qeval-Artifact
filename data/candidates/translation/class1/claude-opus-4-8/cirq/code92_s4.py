# EVAL_META: task_id=92, framework=cirq, class=1
import cirq
import numpy as np

def calculate_stabilizer_state_info():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit()
    circuit.append(cirq.H(q0))
    circuit.append(cirq.CNOT(q0, q1))

    simulator = cirq.Simulator()
    result = simulator.simulate(circuit)
    state_vector = result.final_state_vector

    probabilities_dict = {}
    n = 2
    for i, amp in enumerate(state_vector):
        prob = float(np.abs(amp) ** 2)
        if prob > 1e-12:
            bitstring = format(i, '0{}b'.format(n))
            probabilities_dict[bitstring] = prob

    return probabilities_dict
