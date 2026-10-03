# EVAL_META: task_id=9, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QProg, RY, RZ, CNOT, BARRIER
import numpy as np


def create_efficientSU2():
    num_qubits = 3
    reps = 1

    num_params = num_qubits * 2 * (reps + 1)
    params = [np.pi / 4 * (i + 1) for i in range(num_params)]

    circuit = QCircuit()
    idx = 0

    def su2_layer():
        nonlocal idx
        for q in range(num_qubits):
            circuit << RY(q, params[idx])
            idx += 1
        for q in range(num_qubits):
            circuit << RZ(q, params[idx])
            idx += 1

    def entangle_layer():
        for q in range(num_qubits - 1):
            circuit << CNOT(q, q + 1)

    for rep in range(reps):
        su2_layer()
        circuit << BARRIER(list(range(num_qubits)))
        entangle_layer()
        circuit << BARRIER(list(range(num_qubits)))

    su2_layer()

    prog = QProg()
    prog << circuit
    return prog
