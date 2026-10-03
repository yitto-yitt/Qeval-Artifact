# EVAL_META: task_id=4, framework=qiskit, class=3
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import UnitaryGate


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
    circuit = QuantumCircuit(2)
    circuit.append(gate, [0, 1])
    return circuit
