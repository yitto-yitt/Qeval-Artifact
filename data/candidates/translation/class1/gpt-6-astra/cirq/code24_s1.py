# EVAL_META: task_id=24, framework=cirq, class=1
import cirq
import numpy as np

def dj_algorithm(oracle):
    qubits = list(cirq.QubitOrder.DEFAULT.order_for(oracle.all_qubits()))
    n = len(qubits)
    if n == 0:
        raise ValueError("The oracle must include an output qubit.")

    circuit = cirq.Circuit()
    circuit.append(cirq.X(qubits[-1]))
    circuit.append(cirq.H.on_each(*qubits))
    circuit += oracle
    circuit.append(cirq.H.on_each(*qubits))

    result = cirq.Simulator(dtype=np.complex128).simulate(
        circuit, qubit_order=qubits[::-1]
    )
    probabilities = np.abs(result.final_state_vector) ** 2
    probabilities = probabilities.reshape(2, 2 ** (n - 1)).sum(axis=0)
    probabilities /= probabilities.sum()

    return {
        format(index, f"0{n - 1}b") if n > 1 else "": float(probability)
        for index, probability in enumerate(probabilities)
        if probability > 1e-12
    }
