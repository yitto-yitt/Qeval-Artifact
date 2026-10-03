# EVAL_META: task_id=116, framework=pennylane, class=3
import pennylane as qml
import numpy as np


def synthesize_evolution_gate(pauli_string, time):
    pauli_map = {
        'I': qml.Identity,
        'X': qml.PauliX,
        'Y': qml.PauliY,
        'Z': qml.PauliZ,
    }

    ops = []
    n = len(pauli_string)
    for i, ch in enumerate(pauli_string):
        ops.append(pauli_map[ch](wires=i))

    if len(ops) == 1:
        pauli_op = ops[0]
    else:
        pauli_op = qml.prod(*ops)

    evolution_op = qml.exp(pauli_op, coeff=-1j * time)
    return evolution_op
