# EVAL_META: task_id=112, framework=qiskit, class=3
from qiskit.circuit import QuantumCircuit
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.quantum_info import SparsePauliOp
from qiskit.synthesis import LieTrotter


def create_product_formula_circuit(pauli_strings, times, order, reps):
    pauli_strings = list(pauli_strings)
    times = list(times)

    if len(pauli_strings) == 0:
        return QuantumCircuit(0)

    operator = SparsePauliOp.from_list([(str(pauli), time) for pauli, time in zip(pauli_strings, times)])
    evolution_gate = PauliEvolutionGate(operator, time=1.0)
    synthesizer = LieTrotter(reps=reps)

    return synthesizer.synthesize(evolution_gate)
