# EVAL_META: task_id=117, framework=qpanda, class=3
from pyqpanda3.core import *
import numpy as np

def decompose_unitary(unitary):
    machine = init_quantum_machine(QMachineType.CPU)
    qubits = machine.qAlloc_many(2)
    matrix = np.array(unitary, dtype=complex).tolist()
    circuit = matrix_decompose(qubits, matrix)
    return circuit
