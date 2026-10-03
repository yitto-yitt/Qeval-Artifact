# EVAL_META: task_id=9, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QProg, RY, RZ, CX, BARRIER
import numpy as np


def create_efficientSU2():
    num_qubits = 3
    reps = 1

    num_params = (reps + 1) * num_qubits * 2
    params = [np.pi / 4 * (i + 1) for i in range(num_params)]

    circuit = QCircuit()
    idx = 0

    for _ in range(reps):
        for q in range(num_qubits):
            circuit << RY(q, params[idx]); idx += 1
        for q in range(num_qubits):
            circuit << RZ(q, params[idx]); idx += 1

        circuit << BARRIER(list(range(num_qubits)))

        for i in range(num_qubits - 1):
            for j in range(i + 1, num_qubits):
                circuit << CX(i, j)

        circuit << BARRIER(list(range(num_qubits)))

    for q in range(num_qubits):
        circuit << RY(q, params[idx]); idx += 1
    for q in range(num_qubits):
        circuit << RZ(q, params[idx]); idx += 1

    prog = QProg()
    prog << circuit
    return prog
