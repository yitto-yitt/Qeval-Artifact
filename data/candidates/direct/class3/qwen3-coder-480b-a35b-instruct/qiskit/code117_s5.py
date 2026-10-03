# EVAL_META: task_id=117, framework=qiskit, class=3
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import TwoQubitBasisDecomposer
from qiskit.circuit.library import CXGate


def decompose_unitary(unitary):
    """
    Decompose a 4x4 unitary using the TwoQubitBasisDecomposer with CXGate as the basis gate.

    Args:
        unitary: A 4x4 unitary matrix (numpy array or list)

    Returns:
        QuantumCircuit: The decomposed quantum circuit
    """
    # Create the decomposer with CXGate as the basis gate
    decomposer = TwoQubitBasisDecomposer(CXGate())
    
    # Perform the decomposition
    circuit = decomposer(unitary)
    
    return circuit
