# EVAL_META: task_id=24, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


def dj_algorithm(oracle):
    n = oracle.num_qubits - 1
    if n < 0:
        raise ValueError("The oracle must contain an output qubit.")
    if n == 0:
        return {"": 1.0}

    circuit = QuantumCircuit(n + 1)
    circuit.x(n)
    circuit.h(range(n + 1))
    circuit.compose(oracle, qubits=range(n + 1), inplace=True)
    circuit.h(range(n))

    state = Statevector.from_instruction(circuit)
    probabilities = state.probabilities_dict(qargs=list(range(n)))
    distribution = {
        bitstring: float(probability)
        for bitstring, probability in probabilities.items()
        if probability > 1e-15
    }
    total = sum(distribution.values())
    return {
        bitstring: probability / total
        for bitstring, probability in distribution.items()
    }
