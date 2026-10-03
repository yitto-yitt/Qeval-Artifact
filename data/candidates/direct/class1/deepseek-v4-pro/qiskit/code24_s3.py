# EVAL_META: task_id=24, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.quantum_info import Statevector


def dj_algorithm(oracle):
    n = oracle.num_qubits - 1

    qr = QuantumRegister(n + 1)
    qc = QuantumCircuit(qr)

    # Prepare the output qubit in the |1⟩ state.
    qc.x(qr[n])

    # Apply Hadamard gates to all qubits.
    qc.h(qr)

    # Apply the Deutsch-Jozsa oracle.
    qc.compose(oracle, inplace=True)

    # Apply Hadamard gates to the input qubits only.
    qc.h([qr[i] for i in range(n)])

    # Simulate the final state and compute exact measurement probabilities.
    state = Statevector.from_instruction(qc)

    probabilities = {}
    for idx, amp in enumerate(state.data):
        prob = abs(amp) ** 2
        if prob < 1e-14:
            continue

        # Build bitstring with input qubit n-1 as the leftmost bit,
        # matching Qiskit's standard big-endian measurement key ordering.
        bits = "".join(str((idx >> (n - 1 - j)) & 1) for j in range(n))
        probabilities[bits] = probabilities.get(bits, 0.0) + prob

    # Normalize to remove any tiny floating-point drift.
    total = sum(probabilities.values())
    if total > 0:
        probabilities = {key: value / total for key, value in probabilities.items()}

    return probabilities
