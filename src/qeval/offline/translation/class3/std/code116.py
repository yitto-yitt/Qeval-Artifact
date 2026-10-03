# EVAL_META: task_id=116, framework=qiskit, class=3

from qiskit.circuit.library import PauliEvolutionGate
from qiskit.synthesis import MatrixExponential
from qiskit import QuantumCircuit
from qiskit.quantum_info import Pauli, Operator
import numpy as np

def synthesize_evolution_gate(pauli_string, time):
    pauli = Pauli(pauli_string)
    evolution_gate = PauliEvolutionGate(pauli, time)
    synthesizer = MatrixExponential()
    qc = synthesizer.synthesize(evolution_gate)
    return qc


# ==================================================
