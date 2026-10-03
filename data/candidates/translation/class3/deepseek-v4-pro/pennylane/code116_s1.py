# EVAL_META: task_id=116, framework=pennylane, class=3
import pennylane as qml
from pennylane import numpy as np

def synthesize_evolution_gate(pauli_string, time):
    n_qubits = len(pauli_string)
    dev = qml.device("default.qubit", wires=n_qubits)

    @qml.qnode(dev)
    def circuit():
        qml.PauliRot(2 * time, pauli_string, wires=range(n_qubits))
        return qml.state()
    return circuit
