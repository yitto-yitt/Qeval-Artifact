# EVAL_META: task_id=112, framework=qiskit, class=3
from qiskit.circuit import QuantumCircuit
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.quantum_info import SparsePauliOp
from qiskit.synthesis import LieTrotter, SuzukiTrotter

def create_product_formula_circuit(pauli_strings, times, order, reps):
    hamiltonian = SparsePauliOp.from_list(list(zip(pauli_strings, times)))
    evolution = PauliEvolutionGate(hamiltonian, time=1.0)
    if order == 1:
        synthesis = LieTrotter(reps=reps)
    else:
        synthesis = SuzukiTrotter(order=order, reps=reps)
    return synthesis.synthesize(evolution)
