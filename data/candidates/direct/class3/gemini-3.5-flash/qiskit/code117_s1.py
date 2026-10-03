# EVAL_META: task_id=117, framework=qiskit, class=3

from qiskit.circuit.library import CXGate
from qiskit.synthesis import TwoQubitBasisDecomposer
from qiskit.quantum_info import Operator

def decompose_unitary(unitary):
    """Decompose a 4x4 unitary using the TwoQubitBasisDecomposer with CXGate as the basis gate.
    
    Args:
        unitary: A 4x4 unitary matrix (numpy array or Operator).
        
    Returns:
        QuantumCircuit: The decomposed quantum circuit.
    """
    if not isinstance(unitary, Operator):
        unitary = Operator(unitary)
    decomposer = TwoQubitBasisDecomposer(CXGate())
    return decomposer(unitary)
