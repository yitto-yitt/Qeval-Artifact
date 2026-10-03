# EVAL_META: task_id=4, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit.library import UnitaryGate
import numpy as np

def create_unitary_from_matrix():
    matrix = np.array(
        [
            [0, 0, 0, 1],
            [0, 0, 1, 0],
            [1, 0, 0, 0],
            [0, 1, 0, 0],
        ],
        dtype=complex,
    )
    gate = UnitaryGate(matrix)
    qc = QuantumCircuit(2)
    qc.append(gate, [0, 1])
    return qc
