# EVAL_META: task_id=4, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit.library import UnitaryGate
from qiskit.quantum_info import Operator

def create_unitary_from_matrix():
    matrix = [
        [0, 0, 0, 1],
        [0, 0, 1, 0],
        [1, 0, 0, 0],
        [0, 1, 0, 0],
    ]
    unitary_gate = UnitaryGate(Operator(matrix))
    qc = QuantumCircuit(2)
    qc.append(unitary_gate, [0, 1])
    return qc
