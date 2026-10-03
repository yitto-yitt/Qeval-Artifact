# EVAL_META: task_id=112, framework=qiskit, class=3
from qiskit.circuit import QuantumCircuit
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.quantum_info import SparsePauliOp
from qiskit.synthesis import LieTrotter

def create_product_formula_circuit(pauli_strings, times, order, reps):
    hamiltonian = SparsePauliOp(pauli_strings, coeffs=times)
    evo_gate = PauliEvolutionGate(hamiltonian, time=1.0)
    synthesizer = LieTrotter(order=order, reps=reps)
    circuit = synthesizer.synthesize(evo_gate)
    return circuit
