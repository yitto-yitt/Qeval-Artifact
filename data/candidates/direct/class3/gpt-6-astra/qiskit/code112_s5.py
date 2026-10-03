# EVAL_META: task_id=112, framework=qiskit, class=3
from numbers import Integral

from qiskit import QuantumCircuit
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.quantum_info import SparsePauliOp
from qiskit.synthesis import LieTrotter, SuzukiTrotter


def create_product_formula_circuit(pauli_strings, times, order, reps):
    pauli_strings = list(pauli_strings)
    times = list(times)

    if len(pauli_strings) != len(times):
        raise ValueError("pauli_strings and times must have the same length.")
    if not isinstance(reps, Integral) or isinstance(reps, bool) or reps < 1:
        raise ValueError("reps must be a positive integer.")
    if (
        not isinstance(order, Integral)
        or isinstance(order, bool)
        or order < 1
        or (order != 1 and order % 2 != 0)
    ):
        raise ValueError("order must be 1 or a positive even integer.")

    if not pauli_strings:
        return QuantumCircuit(0)

    if not isinstance(pauli_strings[0], str) or not pauli_strings[0]:
        raise ValueError("Pauli strings must be nonempty strings over I, X, Y, Z.")

    num_qubits = len(pauli_strings[0])
    if any(
        not isinstance(label, str)
        or len(label) != num_qubits
        or any(char not in "IXYZ" for char in label)
        for label in pauli_strings
    ):
        raise ValueError("Pauli strings must have equal length and contain only I, X, Y, Z.")

    formula = (
        LieTrotter(reps=int(reps), preserve_order=True)
        if order == 1
        else SuzukiTrotter(order=int(order), reps=int(reps), preserve_order=True)
    )
    hamiltonian = SparsePauliOp(pauli_strings, coeffs=times)
    evolution = PauliEvolutionGate(hamiltonian, time=1.0, synthesis=formula)
    return formula.synthesize(evolution)
