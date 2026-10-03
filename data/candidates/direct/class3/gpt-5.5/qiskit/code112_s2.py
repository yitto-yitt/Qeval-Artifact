# EVAL_META: task_id=112, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.quantum_info import SparsePauliOp
from qiskit.synthesis import LieTrotter


def create_product_formula_circuit(pauli_strings, times, order, reps):
    if len(pauli_strings) == 0:
        return QuantumCircuit(0)

    terms = [(str(pauli), complex(time)) for pauli, time in zip(pauli_strings, times)]
    operator = SparsePauliOp.from_list(terms)
    evolution_gate = PauliEvolutionGate(operator, time=1.0, synthesis=LieTrotter(reps=reps))
    circuit = QuantumCircuit(operator.num_qubits)
    circuit.append(evolution_gate, range(operator.num_qubits))
    return circuit.decompose()
