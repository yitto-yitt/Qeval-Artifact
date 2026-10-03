# EVAL_META: task_id=116, framework=qiskit, class=3
from qiskit.synthesis import MatrixExponential
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.quantum_info import SparsePauliOp

def synthesize_evolution_gate(pauli_string, time):
    op = SparsePauliOp(pauli_string)
    evo_gate = PauliEvolutionGate(op, time=time)
    synth = MatrixExponential()
    return synth.synthesize(evo_gate)
