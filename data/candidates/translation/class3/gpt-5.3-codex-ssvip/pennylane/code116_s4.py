# EVAL_META: task_id=116, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def synthesize_evolution_gate(pauli_string, time):
    pauli_map = {"I": qml.Identity, "X": qml.PauliX, "Y": qml.PauliY, "Z": qml.PauliZ}
    ops = [pauli_map[p](i) for i, p in enumerate(pauli_string)]
    hamiltonian_op = ops[0]
    for op in ops[1:]:
        hamiltonian_op = hamiltonian_op @ op
    U = qml.matrix(qml.exp(hamiltonian_op, -1j * time))
    return U
