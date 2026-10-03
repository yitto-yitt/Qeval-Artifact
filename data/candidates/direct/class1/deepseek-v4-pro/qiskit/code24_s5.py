# EVAL_META: task_id=24, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


def dj_algorithm(oracle):
    n = oracle.num_qubits - 1
    total_qubits = oracle.num_qubits

    qc = QuantumCircuit(total_qubits)

    qc.x(n)
    qc.h(range(total_qubits))
    qc.compose(oracle, inplace=True)
    qc.h(range(n))

    state = Statevector.from_instruction(qc)
    probabilities = state.probabilities_dict(qargs=list(range(n)))
    return probabilities
