# EVAL_META: task_id=112, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.quantum_info import SparsePauliOp
from qiskit.synthesis import LieTrotter


def create_product_formula_circuit(pauli_strings, times, order, reps):
    if isinstance(pauli_strings, str):
        pauli_strings = [pauli_strings]
    else:
        pauli_strings = list(pauli_strings)

    times = list(times)

    if len(pauli_strings) != len(times):
        raise ValueError("pauli_strings and times must have the same length.")

    if not pauli_strings:
        return QuantumCircuit(0)

    operator = SparsePauliOp(pauli_strings, coeffs=times)
    synthesis = LieTrotter(reps=reps)
    evolution_gate = PauliEvolutionGate(operator, time=1.0, synthesis=synthesis)

    return synthesis.synthesize(evolution_gate)
