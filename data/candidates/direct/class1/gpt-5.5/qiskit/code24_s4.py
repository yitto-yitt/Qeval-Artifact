# EVAL_META: task_id=24, framework=qiskit, class=1

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


def dj_algorithm(oracle):
    total_qubits = int(oracle.num_qubits)
    input_qubits = total_qubits - 1

    if input_qubits == 0:
        return {"": 1.0}

    circuit = QuantumCircuit(total_qubits)
    output_qubit = input_qubits

    circuit.x(output_qubit)
    circuit.h(range(total_qubits))

    if isinstance(oracle, QuantumCircuit):
        circuit.compose(oracle, qubits=list(range(total_qubits)), inplace=True)
    else:
        circuit.append(oracle, list(range(total_qubits)))

    circuit.h(range(input_qubits))

    state = Statevector.from_instruction(circuit)
    mask = (1 << input_qubits) - 1
    distribution = {}

    for index, amplitude in enumerate(state.data):
        probability = abs(amplitude) ** 2
        if probability > 1e-15:
            input_index = index & mask
            bitstring = format(input_index, f"0{input_qubits}b")
            distribution[bitstring] = distribution.get(bitstring, 0.0) + float(probability)

    distribution = {key: value for key, value in distribution.items() if value > 1e-12}
    total_probability = sum(distribution.values())

    result = {}
    for key, value in distribution.items():
        probability = value / total_probability
        if abs(probability - 1.0) < 1e-12:
            probability = 1.0
        result[key] = probability

    return result
