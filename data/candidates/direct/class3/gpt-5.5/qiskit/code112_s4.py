# EVAL_META: task_id=112, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.quantum_info import SparsePauliOp
from qiskit.synthesis import LieTrotter


def create_product_formula_circuit(pauli_strings, times, order, reps):
    if len(pauli_strings) != len(times):
        raise ValueError("pauli_strings and times must have the same length")

    if not pauli_strings:
        return QuantumCircuit(0)

    operator = SparsePauliOp(pauli_strings, coeffs=times)
    num_qubits = operator.num_qubits

    circuit = QuantumCircuit(num_qubits)
    synthesis = LieTrotter(reps=reps)
    evolution_gate = PauliEvolutionGate(operator, time=1.0, synthesis=synthesis)

    circuit.append(evolution_gate, range(num_qubits))
    return circuit
