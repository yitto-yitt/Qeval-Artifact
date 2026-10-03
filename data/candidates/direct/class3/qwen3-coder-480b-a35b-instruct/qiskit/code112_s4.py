# EVAL_META: task_id=112, framework=qiskit, class=3

from qiskit.circuit import QuantumCircuit
from qiskit.opflow import PauliSumOp
from qiskit.synthesis import LieTrotter
import numpy as np


def create_product_formula_circuit(pauli_strings, times, order, reps):
    # Combine all Pauli terms with their respective coefficients (times)
    pauli_terms = []
    for pauli_str, time in zip(pauli_strings, times):
        coeff = time
        from qiskit.quantum_info import Pauli
        pauli_op = Pauli(pauli_str)
        pauli_terms.append((pauli_op, coeff))
    
    # Create a sum of Pauli operators
    op_sum = PauliSumOp.from_list(pauli_terms)
    
    # Use LieTrotter synthesis to build the evolution circuit
    lie_trotter = LieTrotter(reps=reps)
    circuit = lie_trotter.synthesize(op_sum)
    
    return circuit
