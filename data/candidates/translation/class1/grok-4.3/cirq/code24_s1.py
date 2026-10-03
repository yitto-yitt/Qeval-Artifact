# EVAL_META: task_id=24, framework=cirq, class=1
import cirq
import numpy as np

def dj_algorithm(oracle):
    n = oracle.num_qubits
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit(
        cirq.X(qubits[n - 1]),
        cirq.H.on_each(qubits),
        oracle.on(*qubits),
        cirq.H.on_each(qubits),
    )
    sim = cirq.Simulator()
    result = sim.simulate(circuit)
    state = result.final_state_vector
    full_probs = np.abs(state) ** 2
    probs_dict = {}
    n_in = n - 1
    for x in range(1 << n_in):
        p = full_probs[x * 2] + full_probs[x * 2 + 1]
        if p > 1e-8:
            key = bin(x)[2:].zfill(n_in)
            probs_dict[key] = float(p)
    return probs_dict
