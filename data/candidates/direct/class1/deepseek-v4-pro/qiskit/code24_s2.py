# EVAL_META: task_id=24, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


def dj_algorithm(oracle):
    num_qubits = oracle.num_qubits
    n = num_qubits - 1

    qc = QuantumCircuit(num_qubits)

    # Start output qubit in |1>
    qc.x(n)

    # Apply Hadamard to all qubits
    qc.h(list(range(num_qubits)))

    # Apply the oracle
    qc.append(oracle, list(range(num_qubits)))

    # Apply Hadamard to input register
    qc.h(list(range(n)))

    state = Statevector.from_instruction(qc)

    # Return probability distribution of input-register bitstrings.
    # Qiskit bitstring order runs from highest input qubit to qubit 0.
    probs = state.probabilities_dict(qargs=list(range(n - 1, -1, -1)))
    return {key: float(value) for key, value in probs.items()}
