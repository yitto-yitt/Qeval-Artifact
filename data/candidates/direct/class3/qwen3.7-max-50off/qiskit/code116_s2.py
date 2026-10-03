# EVAL_META: task_id=116, framework=qiskit, class=3
from qiskit.circuit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.synthesis import MatrixExponential

def synthesize_evolution_gate(pauli_string, time):
    op = SparsePauliOp(pauli_string)
    evo_gate = PauliEvolutionGate(op, time=time, synthesis=MatrixExponential())
    qc = QuantumCircuit(len(pauli_string))
    qc.append(evo_gate, range(len(pauli_string)))
    return qc
