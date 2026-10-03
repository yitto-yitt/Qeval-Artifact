# EVAL_META: task_id=117, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, Qubit, matrix_decompose

def decompose_unitary(unitary):
    qubits = [Qubit(0), Qubit(1)]
    return matrix_decompose(unitary, qubits)
