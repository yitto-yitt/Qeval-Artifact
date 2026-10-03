# EVAL_META: task_id=12, framework=qiskit, class=3

from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator


def get_unitary():
    circ = QuantumCircuit(2)
    circ.h(0)
    circ.cx(0, 1)
    return Operator.from_circuit(circ).to_matrix()


# ==================================================
