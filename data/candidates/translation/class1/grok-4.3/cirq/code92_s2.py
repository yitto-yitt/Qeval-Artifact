# EVAL_META: task_id=92, framework=cirq, class=1
import cirq
import numpy as np

def calculate_stabilizer_state_info():
    qubits = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(
        cirq.H(qubits[0]),
        cirq.CNOT(qubits[0], qubits[1])
    )
    sim = cirq.Simulator()
    result = sim.simulate(circuit)
    state_vector = result.final_state_vector
    probabilities = np.abs(state_vector)**2
    prob_dict = {}
    for idx, prob in enumerate(probabilities):
        if prob > 1e-10:
            bitstring = format(idx, '02b')
            prob_dict[bitstring] = float(np.round(prob, 10))
    return prob_dict
