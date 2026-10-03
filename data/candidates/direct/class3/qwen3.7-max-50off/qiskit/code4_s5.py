# EVAL_META: task_id=4, framework=qiskit, class=3
from qiskit.circuit import QuantumCircuit
from qiskit.circuit.library import UnitaryGate


def create_unitary_from_matrix():
    matrix = [
        [0, 0, 0, 1],
        [0, 0, 1, 0],
        [1, 0, 0, 0],
        [0, 1, 0, 0]
    ]
    gate = UnitaryGate(matrix)
    qc = QuantumCircuit(2)
    qc.append(gate, [0, 1])
    return qc
