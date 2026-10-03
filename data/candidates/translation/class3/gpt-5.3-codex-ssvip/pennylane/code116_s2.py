# EVAL_META: task_id=116, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def synthesize_evolution_gate(pauli_string, time):
    n = len(pauli_string)
    wire_map = {i: i for i in range(n)}
    op = qml.pauli.string_to_pauli_word(pauli_string, wire_map=wire_map)
    H = qml.matrix(op)
    U = qml.math.expm(-1j * time * H)
    return qml.QubitUnitary(np.array(U), wires=list(range(n)))
