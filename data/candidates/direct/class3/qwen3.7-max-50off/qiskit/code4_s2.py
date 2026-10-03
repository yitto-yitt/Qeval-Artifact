# EVAL_META: task_id=4, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit.library import UnitaryGate


def create_unitary_from_matrix():
    matrix = [
        [0, 0, 0, 1],
        [0, 0, 1, 0],
        [1, 0, 0, 0],
        [0, 1, 0, 0]
    ]

    qc = QuantumCircuit(2)
    gate = UnitaryGate(matrix)
    qc.append(gate, [0, 1])

    return qc
