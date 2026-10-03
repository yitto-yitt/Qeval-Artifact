# EVAL_META: task_id=92, framework=cirq, class=1
import cirq
import numpy as np

def calculate_stabilizer_state_info():
    qubits = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(
        cirq.H(qubits[0]),
        cirq.CNOT(qubits[0], qubits[1]),
    )
    simulator = cirq.CliffordSimulator()
    result = simulator.simulate(circuit)
    state_vector = result.final_state_vector
    probabilities = np.abs(state_vector) ** 2
    n_qubits = 2
    prob_dict = {}
    for i in range(2**n_qubits):
        bitstring = format(i, f'0{n_qubits}b')
        prob_dict[bitstring] = float(probabilities[i])
    return prob_dict
