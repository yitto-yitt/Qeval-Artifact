# EVAL_META: task_id=92, framework=cirq, class=1
import cirq
import numpy as np

def calculate_stabilizer_state_info():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(cirq.H(q0), cirq.CNOT(q0, q1))
    sim = cirq.Simulator()
    result = sim.simulate(circuit)
    state = result.final_state_vector
    probs = np.abs(state) ** 2
    n = len(circuit.all_qubits())
    prob_dict = {}
    for i, p in enumerate(probs):
        if p > 1e-12:
            prob_dict[format(i, f'0{n}b')] = float(p)
    return prob_dict
