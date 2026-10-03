# EVAL_META: task_id=112, framework=qiskit, class=3
from qiskit.synthesis import LieTrotter, SuzukiTrotter
from qiskit.quantum_info import SparsePauliOp
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.circuit import QuantumCircuit


def create_product_formula_circuit(pauli_strings, times, order, reps):
    op = SparsePauliOp(pauli_strings, coeffs=times)

    if order == 1:
        synthesis = LieTrotter(reps=reps)
    else:
        synthesis = SuzukiTrotter(order=order, reps=reps)

    evolution = PauliEvolutionGate(op, time=1.0, synthesis=synthesis)
    qc = QuantumCircuit(op.num_qubits)
    qc.append(evolution, range(op.num_qubits))

    return qc
