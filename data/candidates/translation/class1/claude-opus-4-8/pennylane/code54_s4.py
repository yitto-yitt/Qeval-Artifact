# EVAL_META: task_id=54, framework=pennylane, class=1
import pennylane as qml
from pennylane import numpy as np

def and_gate(a, b):
    a_bits = format(a, '03b')
    b_bits = format(b, '03b')

    # 9 qubits: 0-2 = qr_a, 3-5 = qr_b, 6-8 = ancillary
    dev = qml.device("default.qubit", wires=9)

    @qml.qnode(dev)
    def circuit():
        for i in range(3):
            if a_bits[2 - i] == '1':
                qml.PauliX(wires=i)
            if b_bits[2 - i] == '1':
                qml.PauliX(wires=3 + i)
        for i in range(3):
            qml.Toffoli(wires=[i, 3 + i, 6 + i])
        return qml.probs(wires=[6, 7, 8])

    probs = circuit()
    num_states = 2 ** 3
    result = {}
    for idx in range(num_states):
        if probs[idx] > 0:
            key = format(idx, '03b')
            result[key] = float(probs[idx])
    return result
