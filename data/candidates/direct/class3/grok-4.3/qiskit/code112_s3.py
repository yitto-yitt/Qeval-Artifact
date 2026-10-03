# EVAL_META: task_id=112, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.synthesis import LieTrotter

def create_product_formula_circuit(pauli_strings, times, order, reps):
    op = SparsePauliOp.from_list(list(zip(pauli_strings, times)))
    num_qubits = op.num_qubits
    trotter = LieTrotter(reps=reps)
    evo_gate = PauliEvolutionGate(op, time=1.0, synthesis=trotter)
    qc = QuantumCircuit(num_qubits)
    qc.append(evo_gate, range(num_qubits))
    return qc.decompose()
