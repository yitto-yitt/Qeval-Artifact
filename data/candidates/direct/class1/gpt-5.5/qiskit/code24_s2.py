# EVAL_META: task_id=24, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


def dj_algorithm(oracle):
    total_qubits = oracle.num_qubits
    input_qubits = total_qubits - 1

    circuit = QuantumCircuit(total_qubits)

    for qubit in range(input_qubits):
        circuit.h(qubit)

    circuit.x(input_qubits)
    circuit.h(input_qubits)

    if isinstance(oracle, QuantumCircuit):
        circuit.compose(oracle, qubits=list(range(total_qubits)), inplace=True)
    else:
        circuit.append(oracle, list(range(total_qubits)))

    for qubit in range(input_qubits):
        circuit.h(qubit)

    state = Statevector.from_instruction(circuit)
    probabilities = {}

    for index, amplitude in enumerate(state.data):
        probability = float(abs(amplitude) ** 2)
        if probability <= 1e-12:
            continue

        bitstring = "".join(
            "1" if (index >> qubit) & 1 else "0"
            for qubit in range(input_qubits - 1, -1, -1)
        )
        probabilities[bitstring] = probabilities.get(bitstring, 0.0) + probability

    cleaned = {}
    for bitstring in sorted(probabilities):
        probability = probabilities[bitstring]
        if abs(probability) <= 1e-12:
            continue
        if abs(probability - 1.0) <= 1e-12:
            probability = 1.0
        cleaned[bitstring] = float(probability)

    return cleaned
