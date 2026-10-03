# EVAL_META: task_id=39, framework=qiskit, class=2
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

def create_uniform_superposition(n):
    if n == 0:
        return Statevector([1.0 + 0.0j])
    qc = QuantumCircuit(n)
    qc.h(range(n))
    return Statevector.from_instruction(qc)
