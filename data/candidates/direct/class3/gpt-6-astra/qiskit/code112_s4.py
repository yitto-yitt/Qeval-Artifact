# EVAL_META: task_id=112, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.quantum_info import Pauli
from qiskit.synthesis import LieTrotter


def create_product_formula_circuit(pauli_strings, times, order, reps):
    pauli_strings = list(pauli_strings)
    times = list(times)

    if len(pauli_strings) != len(times):
        raise ValueError("Each Pauli string must have a corresponding time.")
    if not isinstance(reps, int) or isinstance(reps, bool) or reps < 1:
        raise ValueError("reps must be a positive integer.")
    if not pauli_strings:
        return QuantumCircuit()

    paulis = [Pauli(label) for label in pauli_strings]
    num_qubits = paulis[0].num_qubits
    if any(pauli.num_qubits != num_qubits for pauli in paulis):
        raise ValueError("All Pauli strings must have the same length.")

    circuit = QuantumCircuit(num_qubits)
    formula = LieTrotter(reps=reps)

    for pauli, time in zip(paulis, times):
        evolution = PauliEvolutionGate(pauli, time=time, synthesis=formula)
        circuit.compose(formula.synthesize(evolution), inplace=True)

    return circuit
