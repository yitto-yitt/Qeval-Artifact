# EVAL_META: task_id=117, framework=qiskit, class=3
from qiskit.circuit.library import CXGate
from qiskit.quantum_info import Operator
try:
    from qiskit.synthesis.two_qubit.two_qubit_decompose import TwoQubitBasisDecomposer
except ImportError:
    from qiskit.quantum_info.synthesis.two_qubit_decompose import TwoQubitBasisDecomposer


def decompose_unitary(unitary):
    decomposer = TwoQubitBasisDecomposer(CXGate())
    circuit = decomposer(Operator(unitary))
    return circuit
