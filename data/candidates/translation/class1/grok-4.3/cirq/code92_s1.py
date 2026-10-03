# EVAL_META: task_id=92, framework=cirq, class=1
import cirq
import numpy as np

def calculate_stabilizer_state_info():
    qubits = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(cirq.H(qubits[0]), cirq.CNOT(qubits[0], qubits[1]))
    state_vector = cirq.final_state_vector(circuit)
    probabilities = np.abs(state_vector) ** 2
    prob_dict = {}
    n_qubits = 2
    for i, prob in enumerate(probabilities):
        if prob > 1e-8:
            bitstring = bin(i)[2:].zfill(n_qubits)
            prob_dict[bitstring] = float(np.round(prob, decimals=10))
    return prob_dict
