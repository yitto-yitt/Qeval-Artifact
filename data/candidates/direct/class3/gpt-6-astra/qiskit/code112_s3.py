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
    if any(len(pauli) != len(pauli_strings[0]) for pauli in pauli_strings):
        raise ValueError("All Pauli strings must have the same length.")
    if not isinstance(reps, int) or isinstance(reps, bool) or reps < 1:
        raise ValueError("reps must be a positive integer.")
    if not isinstance(order, int) or isinstance(order, bool):
        raise ValueError("order must be 1 or a positive even integer.")

    if order == 1:
        synthesis = LieTrotter(reps=reps, preserve_order=True)
    elif order >= 2 and order % 2 == 0:
        synthesis = SuzukiTrotter(order=order, reps=reps, preserve_order=True)
    else:
        raise ValueError("order must be 1 or a positive even integer.")

    operator = SparsePauliOp.from_list(list(zip(pauli_strings, times)))
    evolution = PauliEvolutionGate(operator, time=1.0, synthesis=synthesis)
    return synthesis.synthesize(evolution)
