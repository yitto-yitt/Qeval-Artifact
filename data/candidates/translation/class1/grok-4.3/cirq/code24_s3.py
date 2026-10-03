# EVAL_META: task_id=24, framework=cirq, class=1
import cirq
import numpy as np

def dj_algorithm(oracle):
    qubits = sorted(oracle.qubits)
    n = len(qubits)
    circuit = cirq.Circuit(
        cirq.X(qubits[-1]),
        cirq.H.on_each(qubits),
        oracle,
        cirq.H.on_each(qubits),
    )
    sim = cirq.Simulator()
    result = sim.simulate(circuit)
    state = result.final_state_vector
    dim_input = 2 ** (n - 1)
    state_reshaped = state.reshape((dim_input, 2))
    probs = np.abs(state_reshaped) ** 2
    input_probs = probs.sum(axis=1)
    prob_dict = {}
    for i in range(dim_input):
        p = float(input_probs[i])
        if p > 1e-10:
            bitstring = format(i, f'0{n-1}b')
            prob_dict[bitstring] = p
    return prob_dict
