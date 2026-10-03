# EVAL_META: task_id=24, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


def dj_algorithm(oracle):
    num_qubits = oracle.num_qubits
    num_inputs = num_qubits - 1
    output_qubit = num_inputs

    circuit = QuantumCircuit(num_qubits)

    circuit.x(output_qubit)
    circuit.h(output_qubit)

    for qubit in range(num_inputs):
        circuit.h(qubit)

    if isinstance(oracle, QuantumCircuit):
        circuit.compose(oracle, qubits=list(range(num_qubits)), inplace=True)
    else:
        circuit.append(oracle, list(range(num_qubits)))

    for qubit in range(num_inputs):
        circuit.h(qubit)

    state = Statevector.from_instruction(circuit)
    probabilities = {}

    for basis_index, amplitude in enumerate(state.data):
        probability = float(abs(amplitude) ** 2)
        if probability > 1e-12:
            bitstring = "".join(str((basis_index >> qubit) & 1) for qubit in reversed(range(num_inputs)))
            probabilities[bitstring] = probabilities.get(bitstring, 0.0) + probability

    total = sum(probabilities.values())
    if total:
        probabilities = {key: value / total for key, value in probabilities.items()}

    return probabilities
