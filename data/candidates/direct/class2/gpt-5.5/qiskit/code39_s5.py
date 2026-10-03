# EVAL_META: task_id=39, framework=qiskit, class=2
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


def create_uniform_superposition(n):
    circuit = QuantumCircuit(n)
    circuit.h(range(n))
    return Statevector.from_instruction(circuit)
