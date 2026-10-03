# EVAL_META: task_id=116, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def synthesize_evolution_gate(pauli_string, time):
    pauli_map = {'I': qml.Identity, 'X': qml.PauliX, 'Y': qml.PauliY, 'Z': qml.PauliZ}
    n = len(pauli_string)

    ops = [pauli_map[p](i) for i, p in enumerate(pauli_string)]
    obs = ops[0]
    for o in ops[1:]:
        obs = obs @ o

    H = qml.Hamiltonian([1.0], [obs])

    dev = qml.device("default.qubit", wires=n)

    @qml.qnode(dev)
    def circuit():
        qml.evolve(H, time)
        return qml.state()

    return circuit
