# EVAL_META: task_id=12, framework=qiskit, class=3

from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator


def get_unitary():
    circuit = QuantumCircuit(2)
    circuit.h(0)
    circuit.cx(0, 1)
    return Operator(circuit).data
