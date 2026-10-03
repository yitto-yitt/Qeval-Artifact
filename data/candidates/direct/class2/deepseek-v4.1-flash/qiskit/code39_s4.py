# EVAL_META: task_id=39, framework=qiskit, class=2
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


def create_uniform_superposition(n):
    qc = QuantumCircuit(n)
    qc.h(range(n))
    return Statevector(qc)
