# EVAL_META: task_id=117, framework=qiskit, class=3
from qiskit.synthesis import TwoQubitBasisDecomposer
from qiskit.circuit.library import CXGate
from qiskit.quantum_info import Operator


def decompose_unitary(unitary):
    decomposer = TwoQubitBasisDecomposer(CXGate())
    op = unitary if isinstance(unitary, Operator) else Operator(unitary)
    return decomposer(op)
