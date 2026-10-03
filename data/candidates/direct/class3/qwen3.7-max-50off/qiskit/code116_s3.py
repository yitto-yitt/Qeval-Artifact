# EVAL_META: task_id=116, framework=qiskit, class=3
from qiskit.circuit import QuantumCircuit
from qiskit.quantum_info import Pauli
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.synthesis import MatrixExponential

def synthesize_evolution_gate(pauli_string, time):
    pauli = Pauli(pauli_string)
    synthesis = MatrixExponential()
    evo_gate = PauliEvolutionGate(pauli, time, synthesis=synthesis)
    qc = QuantumCircuit(pauli.num_qubits)
    qc.append(evo_gate, range(pauli.num_qubits))
    return qc
