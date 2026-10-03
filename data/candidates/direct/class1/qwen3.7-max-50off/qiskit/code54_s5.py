# EVAL_META: task_id=54, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


def and_gate(a, b):
    qc = QuantumCircuit(9)

    # Encode a into qubits 0, 1, 2
    for i in range(3):
        if (a >> i) & 1:
            qc.x(i)

    # Encode b into qubits 3, 4, 5
    for i in range(3):
        if (b >> i) & 1:
            qc.x(3 + i)

    # Bitwise AND using Toffoli gates, result in qubits 6, 7, 8
    for i in range(3):
        qc.ccx(i, 3 + i, 6 + i)

    # Get probability distribution over output qubits
    sv = Statevector.from_instruction(qc)
    probs = sv.probabilities_dict(qargs=[6, 7, 8])

    result = {}
    for state, prob in probs.items():
        if prob > 1e-9:
            result[state] = prob

    return result
