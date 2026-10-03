# EVAL_META: task_id=24, framework=cirq, class=1
import cirq
import numpy as np

def dj_algorithm(oracle):
    n = oracle.num_qubits
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit()
    circuit.append(cirq.X(qubits[n-1]))
    circuit.append(cirq.H.on_each(qubits))
    circuit.append(oracle.on(*qubits))
    circuit.append(cirq.H.on_each(qubits))
    sim = cirq.Simulator()
    state_vector = sim.simulate(circuit).final_state_vector
    prob_map = {}
    for i in range(2 ** (n - 1)):
        prob = 0.0
        for out in [0, 1]:
            full_idx = (i << 1) | out
            prob += np.abs(state_vector[full_idx]) ** 2
        key = format(i, f'0{n-1}b')
        prob_map[key] = float(prob)
    return prob_map
