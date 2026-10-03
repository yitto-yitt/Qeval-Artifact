# EVAL_META: task_id=112, framework=qiskit, class=3
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.quantum_info import SparsePauliOp
from qiskit.synthesis import LieTrotter, SuzukiTrotter


def create_product_formula_circuit(pauli_strings, times, order, reps):
    pauli_strings = list(pauli_strings)
    times = list(times)

    if not pauli_strings:
        raise ValueError("pauli_strings must not be empty.")
    if len(pauli_strings) != len(times):
        raise ValueError("Each Pauli string must have a corresponding time.")
    if not isinstance(reps, int) or isinstance(reps, bool) or reps < 1:
        raise ValueError("reps must be a positive integer.")
    if (
        not isinstance(order, int)
        or isinstance(order, bool)
        or order < 1
        or (order != 1 and order % 2 != 0)
    ):
        raise ValueError("order must be 1 or a positive even integer.")

    num_qubits = len(pauli_strings[0])
    if num_qubits == 0 or any(
        len(pauli) != num_qubits or any(char not in "IXYZ" for char in pauli)
        for pauli in pauli_strings
    ):
        raise ValueError("Pauli strings must have equal nonzero lengths and use I, X, Y, Z.")

    hamiltonian = SparsePauliOp(pauli_strings, coeffs=times)
    synthesis = (
        LieTrotter(reps=reps)
        if order == 1
        else SuzukiTrotter(order=order, reps=reps)
    )
    evolution = PauliEvolutionGate(hamiltonian, time=1.0, synthesis=synthesis)
    return synthesis.synthesize(evolution)
