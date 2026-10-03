# EVAL_META: task_id=9, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QGate, RY, RZ, CNOT, BARRIER
import numpy as np


def create_efficientSU2():
    num_qubits = 3
    reps = 1

    params = [f"θ[{i}]" for i in range(num_qubits * 2 * (reps + 1))]
    p_idx = 0

    circuit = QCircuit()

    def rotation_layer():
        nonlocal p_idx
        for q in range(num_qubits):
            circuit << RY(q, 0.0)
            p_idx += 1
        for q in range(num_qubits):
            circuit << RZ(q, 0.0)
            p_idx += 1

    def entanglement_layer():
        for q in range(num_qubits - 1):
            circuit << CNOT(q, q + 1)

    for r in range(reps):
        rotation_layer()
        circuit << BARRIER(list(range(num_qubits)))
        entanglement_layer()
        circuit << BARRIER(list(range(num_qubits)))

    rotation_layer()

    return circuit
