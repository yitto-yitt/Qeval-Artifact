# EVAL_META: task_id=92, framework=cirq, class=1
import cirq
import numpy as np

def calculate_stabilizer_state_info():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(
        cirq.H(q0),
        cirq.CNOT(q0, q1),
    )
    simulator = cirq.Simulator(dtype=np.complex128)
    result = simulator.simulate(circuit, qubit_order=[q0, q1])
    state_vector = result.final_state_vector
    probabilities = np.abs(state_vector) ** 2

    probabilities_dict = {}
    num_qubits = 2
    for index, probability in enumerate(probabilities):
        if probability > 1e-12:
            bitstring = format(index, f"0{num_qubits}b")
            probabilities_dict[bitstring] = float(np.round(probability, 12))
    return probabilities_dict
