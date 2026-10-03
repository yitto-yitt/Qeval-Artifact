# EVAL_META: task_id=116, framework=pennylane, class=3
import pennylane as qml
import numpy as np


def synthesize_evolution_gate(pauli_string, time):
    n = len(pauli_string)
    pauli_map = {
        'I': qml.Identity,
        'X': qml.PauliX,
        'Y': qml.PauliY,
        'Z': qml.PauliZ,
    }

    op = None
    for i, ch in enumerate(pauli_string):
        wire = n - 1 - i
        term = pauli_map[ch](wire)
        op = term if op is None else op @ term

    evolution_op = qml.exp(op, coeff=-1j * time)

    def circuit():
        qml.apply(evolution_op)
        return evolution_op

    circuit.operation = evolution_op
    circuit.matrix = lambda: qml.matrix(evolution_op, wire_order=list(range(n)))
    return circuit
