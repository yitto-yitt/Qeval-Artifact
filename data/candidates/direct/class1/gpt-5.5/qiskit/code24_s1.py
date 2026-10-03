# EVAL_META: task_id=24, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


def dj_algorithm(oracle):
    total_qubits = oracle.num_qubits
    input_qubits = total_qubits - 1
    output_qubit = input_qubits

    circuit = QuantumCircuit(total_qubits)

    circuit.x(output_qubit)
    for qubit in range(total_qubits):
        circuit.h(qubit)

    if isinstance(oracle, QuantumCircuit):
        circuit.append(oracle.to_instruction(), list(range(total_qubits)))
    else:
        circuit.append(oracle, list(range(total_qubits)))

    for qubit in range(input_qubits):
        circuit.h(qubit)

    state = Statevector.from_instruction(circuit)
    full_probs = state.probabilities_dict()

    distribution = {}
    for bitstring, probability in full_probs.items():
        input_bitstring = bitstring[1:] if input_qubits > 0 else ""
        distribution[input_bitstring] = distribution.get(input_bitstring, 0.0) + float(probability)

    cleaned = {}
    for bitstring, probability in distribution.items():
        if abs(probability) > 1e-12:
            if abs(probability - 1.0) < 1e-12:
                probability = 1.0
            cleaned[bitstring] = probability

    return cleaned
