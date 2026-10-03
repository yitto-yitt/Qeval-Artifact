# EVAL_META: task_id=39, framework=qiskit, class=2

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

def create_uniform_superposition(n: int) -> Statevector:
    """
    Initialize a uniform superposition on n qubits and return its statevector.
    """
    qc = QuantumCircuit(n)
    if n > 0:
        qc.h(range(n))
    return Statevector(qc)
