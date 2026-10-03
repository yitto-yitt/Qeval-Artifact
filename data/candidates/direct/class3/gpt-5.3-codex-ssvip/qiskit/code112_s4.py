# EVAL_META: task_id=112, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit.synthesis import LieTrotter


def create_product_formula_circuit(pauli_strings, times, order, reps):
    if len(pauli_strings) != len(times):
        raise ValueError("pauli_strings and times must have the same length.")
    if len(pauli_strings) == 0:
        return QuantumCircuit(0)

    num_qubits = len(pauli_strings[0])
    for p in pauli_strings:
        if len(p) != num_qubits:
            raise ValueError("All pauli strings must have the same length.")

    labels = []
    coeffs = []
    for p, t in zip(pauli_strings, times):
        labels.append(p)
        coeffs.append(float(t))

    op = SparsePauliOp(labels, coeffs=coeffs)
    synthesizer = LieTrotter(reps=reps, order=order)
    return synthesizer.synthesize(op)
