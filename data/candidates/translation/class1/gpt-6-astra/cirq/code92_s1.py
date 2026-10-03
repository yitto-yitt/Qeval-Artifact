# EVAL_META: task_id=92, framework=cirq, class=1
import cirq
import numpy as np

def calculate_stabilizer_state_info():
    qubits = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(
        cirq.H(qubits[0]),
        cirq.CNOT(qubits[0], qubits[1]),
    )
    result = cirq.Simulator(dtype=np.complex128).simulate(
        circuit, qubit_order=qubits
    )
    probabilities = np.abs(result.final_state_vector) ** 2
    return {
        format(index, "02b")[::-1]: float(probability)
        for index, probability in enumerate(probabilities)
        if probability > 0
    }
