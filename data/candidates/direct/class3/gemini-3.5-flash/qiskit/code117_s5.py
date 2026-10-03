# EVAL_META: task_id=117, framework=qiskit, class=3
from qiskit.circuit.library import CXGate
try:
    from qiskit.synthesis import TwoQubitBasisDecomposer
except ImportError:
    from qiskit.quantum_info import TwoQubitBasisDecomposer

def decompose_unitary(unitary):
    """
    Decompose a 4x4 unitary using the TwoQubitBasisDecomposer with CXGate as the basis gate.
    
    Args:
        unitary (np.ndarray or Operator): The 4x4 unitary matrix to decompose.
        
    Returns:
        QuantumCircuit: The resulting quantum circuit.
    """
    decomposer = TwoQubitBasisDecomposer(CXGate())
    return decomposer(unitary)
