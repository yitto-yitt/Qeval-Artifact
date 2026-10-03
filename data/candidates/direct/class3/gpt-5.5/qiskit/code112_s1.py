# EVAL_META: task_id=112, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.quantum_info import SparsePauliOp
from qiskit.synthesis import LieTrotter


def create_product_formula_circuit(pauli_strings, times, order, reps):
    if len(pauli_strings) != len(times):
        raise ValueError("pauli_strings and times must have the same length")

    if len(pauli_strings) == 0:
        return QuantumCircuit(0)

    operator = SparsePauliOp.from_list([(str(pauli), coeff) for pauli, coeff in zip(pauli_strings, times)])
    synthesis = LieTrotter(reps=reps)
    evolution_gate = PauliEvolutionGate(operator, time=1.0, synthesis=synthesis)
    return synthesis.synthesize(evolution_gate)
