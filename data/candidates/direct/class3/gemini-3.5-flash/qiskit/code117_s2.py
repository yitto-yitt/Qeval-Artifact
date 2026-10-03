# EVAL_META: task_id=117, framework=qiskit, class=3
from qiskit.synthesis import TwoQubitBasisDecomposer
from qiskit.circuit.library import CXGate

def decompose_unitary(unitary):
    """Decompose a 4x4 unitary using TwoQubitBasisDecomposer with CXGate as the basis."""
    decomposer = TwoQubitBasisDecomposer(CXGate())
    return decomposer(unitary)
