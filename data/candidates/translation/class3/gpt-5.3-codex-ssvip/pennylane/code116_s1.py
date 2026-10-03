# EVAL_META: task_id=116, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def synthesize_evolution_gate(pauli_string, time):
    n_qubits = len(pauli_string)
    dev = qml.device("default.qubit", wires=n_qubits)

    pauli_map = {
        "I": qml.Identity,
        "X": qml.PauliX,
        "Y": qml.PauliY,
        "Z": qml.PauliZ,
    }

    ops = [pauli_map[p](wires=i) for i, p in enumerate(pauli_string)]
    H = qml.prod(*ops) if len(ops) > 1 else ops[0]

    @qml.qnode(dev)
    def circuit():
        qml.exp(H, coeff=-1j * time)
        return qml.state()

    circuit()
    return circuit.qtape.operations
