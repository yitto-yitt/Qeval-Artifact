# EVAL_META: task_id=116, framework=qiskit, class=3
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit.synthesis import EvolutionSynthesis


def synthesize_evolution_gate(pauli_string, time):
    # Create a SparsePauliOp from the pauli string
    pauli_op = SparsePauliOp(pauli_string)
    
    # Create an evolution synthesis object
    from qiskit.synthesis.evolution import MatrixExponential
    synthesis = MatrixExponential()
    
    # Synthesize the evolution circuit
    circuit = synthesis.synthesize(pauli_op, time)
    
    return circuit
