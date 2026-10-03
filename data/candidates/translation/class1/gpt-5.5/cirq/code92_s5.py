# EVAL_META: task_id=92, framework=cirq, class=1
import cirq
import numpy as np

def calculate_stabilizer_state_info():
    qubits = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(
        cirq.H(qubits[0]),
        cirq.CNOT(qubits[0], qubits[1]),
    )
    simulator = cirq.Simulator()
    result = simulator.simulate(circuit, qubit_order=qubits)
    state_vector = result.final_state_vector
    probabilities = np.abs(state_vector) ** 2

    probabilities_dict = {}
    num_qubits = len(qubits)
    for index, probability in enumerate(probabilities):
        if probability > 1e-12:
            bitstring = format(index, f"0{num_qubits}b")
            probabilities_dict[bitstring] = float(round(float(probability), 12))
    return probabilities_dict
