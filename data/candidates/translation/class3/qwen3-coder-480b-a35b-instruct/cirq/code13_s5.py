# EVAL_META: task_id=13, framework=cirq, class=3
import cirq
import numpy as np

def custom_rotation_gate():
    qubit = cirq.LineQubit(0)
    circuit = cirq.Circuit()
    circuit.append(cirq.rz(np.pi / 2).on(qubit))
    circuit.append(cirq.ry(np.pi / 2).on(qubit))
    circuit.append(cirq.rz(np.pi / 2).on(qubit))
    return circuit
