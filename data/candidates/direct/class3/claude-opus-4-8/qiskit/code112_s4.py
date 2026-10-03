# EVAL_META: task_id=112, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.synthesis import LieTrotter


def create_product_formula_circuit(pauli_strings, times, order, reps):
    num_qubits = len(pauli_strings[0])
    operator = SparsePauliOp.from_list(
        [(p, t) for p, t in zip(pauli_strings, times)]
    )
    synth = LieTrotter(reps=reps)
    evo_gate = PauliEvolutionGate(operator, time=1.0, synthesis=synth)
    circuit = QuantumCircuit(num_qubits)
    circuit.append(evo_gate, range(num_qubits))
    return circuit
