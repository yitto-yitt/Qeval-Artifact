# EVAL_META: task_id=39, framework=qiskit, class=2
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


def create_uniform_superposition(n):
    qc = QuantumCircuit(n)
    for q in range(n):
        qc.h(q)
    return Statevector.from_instruction(qc)
