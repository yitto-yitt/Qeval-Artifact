# EVAL_META: task_id=112, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.synthesis import LieTrotter


def create_product_formula_circuit(pauli_strings, times, order, reps):
    num_qubits = len(pauli_strings[0])
    circuit = QuantumCircuit(num_qubits)
    synth = LieTrotter(reps=reps)
    for pauli, time in zip(pauli_strings, times):
        operator = SparsePauliOp.from_list([(pauli, 1.0)])
        gate = PauliEvolutionGate(operator, time=time, synthesis=synth)
        circuit.append(gate, range(num_qubits))
    return circuit
