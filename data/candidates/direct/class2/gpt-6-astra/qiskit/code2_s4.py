# EVAL_META: task_id=2, framework=qiskit, class=2
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


def create_bell_statevector():
    circuit = QuantumCircuit(2)
    circuit.h(0)
    circuit.cx(0, 1)
    return Statevector.from_instruction(circuit)
