# EVAL_META: task_id=12, framework=qpanda, class=3
from pyqpanda3.core import init, finalize, qAlloc_many, QProg, H, CNOT, get_matrix, QuantumMachineType


def get_unitary():
    init(QuantumMachineType.CPU)
    try:
        qubits = qAlloc_many(2)
        prog = QProg()
        prog << H(qubits[0]) << CNOT(qubits[0], qubits[1])
        matrix = get_matrix(prog, qubits)
        return matrix.copy()
    finally:
        finalize()
