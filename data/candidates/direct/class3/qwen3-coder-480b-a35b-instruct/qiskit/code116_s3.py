# EVAL_META: task_id=116, framework=qiskit, class=3
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp, Operator
from qiskit.circuit.library import PauliEvolutionGate


def synthesize_evolution_gate(pauli_string, time):
    """
    Synthesizes an evolution gate using MatrixExponential for a given Pauli string and time.
    
    Args:
        pauli_string (str): A string containing Pauli operators ('I', 'X', 'Y', 'Z')
        time (float): Evolution time
    
    Returns:
        QuantumCircuit: Circuit implementing the evolution gate
    """
    # Create a SparsePauliOp from the pauli string
    pauli_op = SparsePauliOp(pauli_string)
    
    # Create the evolution gate
    evolution_gate = PauliEvolutionGate(pauli_op, time=time)
    
    # Create a quantum circuit with the number of qubits equal to the length of the pauli string
    num_qubits = len(pauli_string)
    qc = QuantumCircuit(num_qubits)
    
    # Append the evolution gate to the circuit
    qc.append(evolution_gate, range(num_qubits))
    
    return qc
