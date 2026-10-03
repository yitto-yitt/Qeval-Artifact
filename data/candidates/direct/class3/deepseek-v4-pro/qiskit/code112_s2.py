# EVAL_META: task_id=112, framework=qiskit, class=3

from qiskit.quantum_info import SparsePauliOp
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.synthesis import LieTrotter, SuzukiTrotter


def create_product_formula_circuit(pauli_strings, times, order, reps):
    operator = SparsePauliOp(pauli_strings, coeffs=times)
    evolution_gate = PauliEvolutionGate(operator, time=1.0)

    if order == 1:
        synth = LieTrotter(reps=reps)
    else:
        synth = SuzukiTrotter(order=order, reps=reps)

    return synth.synthesize(evolution_gate)
