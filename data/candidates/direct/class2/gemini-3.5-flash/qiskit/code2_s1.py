# EVAL_META: task_id=2, framework=qiskit, class=2

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

def create_bell_statevector():
    """
    Returns a Phi+ Bell statevector: (|00> + |11>) / sqrt(2)
    """
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    return Statevector.from_instruction(qc)
