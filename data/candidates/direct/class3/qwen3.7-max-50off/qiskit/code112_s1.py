# EVAL_META: task_id=112, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.synthesis import LieTrotter

def create_product_formula_circuit(pauli_strings, times, order, reps):
    op = SparsePauliOp(pauli_strings, coeffs=times)
    synthesis = LieTrotter(reps=reps)
    evo_gate = PauliEvolutionGate(op, time=1.0, synthesis=synthesis)
    qc = QuantumCircuit(op.num_qubits)
    qc.append(evo_gate, range(op.num_qubits))
    return qc
