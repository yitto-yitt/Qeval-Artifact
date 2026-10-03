# EVAL_META: task_id=112, framework=qiskit, class=3

from qiskit.circuit import QuantumCircuit
from qiskit.opflow import PauliSumOp
from qiskit.synthesis import LieTrotter
import numpy as np


def create_product_formula_circuit(pauli_strings, times, order, reps):
    """
    Creates a quantum circuit using Lie-Trotter product formula for a list of Pauli strings and times.

    Args:
        pauli_strings: List of Pauli strings (e.g., ['XX', 'YY', 'ZZ'])
        times: List of corresponding times for each Pauli string
        order: Order of the product formula (for LieTrotter it's typically 1)
        reps: Number of repetitions of the Trotter step

    Returns:
        QuantumCircuit: The resulting quantum circuit
    """
    if len(pauli_strings) != len(times):
        raise ValueError("Length of pauli_strings and times must be equal")

    # Build the Hamiltonian as a sum of Pauli terms
    pauli_ops = []
    for pauli_str, time in zip(pauli_strings, times):
        # Create a Pauli operator from the string
        coeff = time
        # Convert the Pauli string to a proper operator
        from qiskit.quantum_info import SparsePauliOp
        pauli_op = SparsePauliOp(pauli_str)
        pauli_ops.append(coeff * pauli_op)

    # Sum all the operators
    hamiltonian = sum(pauli_ops)

    # Create the evolution circuit using Lie-Trotter
    lie_trotter = LieTrotter(reps=reps)
    
    # Synthesize the evolution circuit
    evolution_circuit = lie_trotter.synthesize(hamiltonian.to_pauli_op())

    return evolution_circuit
