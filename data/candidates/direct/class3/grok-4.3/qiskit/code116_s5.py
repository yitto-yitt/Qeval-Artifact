# EVAL_META: task_id=116, framework=qiskit, class=3
from qiskit.quantum_info import SparsePauliOp
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.synthesis import MatrixExponential

def synthesize_evolution_gate(pauli_string, time):
    hamiltonian = SparsePauliOp(pauli_string)
    evo = PauliEvolutionGate(hamiltonian, time=time)
    synth = MatrixExponential()
    return synth.synthesize(evo)
