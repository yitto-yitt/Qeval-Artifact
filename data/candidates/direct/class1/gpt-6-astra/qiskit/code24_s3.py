# EVAL_META: task_id=24, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


def dj_algorithm(oracle):
    num_qubits = oracle.num_qubits
    if num_qubits < 1:
        raise ValueError("The oracle must include an output qubit.")

    num_inputs = num_qubits - 1
    circuit = QuantumCircuit(num_qubits)
    circuit.x(num_inputs)
    circuit.h(range(num_qubits))
    circuit.compose(oracle, qubits=range(num_qubits), inplace=True)
    if num_inputs:
        circuit.h(range(num_inputs))

    state = Statevector.from_instruction(circuit)
    if not num_inputs:
        return {"": 1.0}

    probabilities = state.probabilities(qargs=list(range(num_inputs)))
    distribution = {
        format(index, f"0{num_inputs}b"): float(probability)
        for index, probability in enumerate(probabilities)
        if probability > 1e-15
    }
    total = sum(distribution.values())
    return {bitstring: probability / total for bitstring, probability in distribution.items()}
