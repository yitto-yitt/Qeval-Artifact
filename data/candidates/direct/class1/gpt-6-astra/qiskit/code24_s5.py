# EVAL_META: task_id=24, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


def dj_algorithm(oracle):
    num_qubits = oracle.num_qubits
    if num_qubits < 2:
        raise ValueError("The oracle must have at least one input and one output qubit.")

    num_inputs = num_qubits - 1
    inputs = list(range(num_inputs))
    circuit = QuantumCircuit(num_qubits)

    circuit.x(num_inputs)
    circuit.h(range(num_qubits))
    circuit.compose(oracle, qubits=list(range(num_qubits)), inplace=True)
    circuit.h(inputs)

    probabilities = Statevector.from_instruction(circuit).probabilities_dict(
        qargs=inputs
    )
    distribution = {
        bitstring: float(probability)
        for bitstring, probability in probabilities.items()
        if probability > 1e-12
    }
    total = sum(distribution.values())
    return {
        bitstring: probability / total
        for bitstring, probability in distribution.items()
    }
