# EVAL_META: task_id=116, framework=pennylane, class=3
import pennylane as qml

def synthesize_evolution_gate(pauli_string, time):
    num_wires = len(pauli_string)
    dev = qml.device("default.qubit", wires=num_wires)

    @qml.qnode(dev)
    def circuit():
        qml.PauliRot(2 * time, pauli_string, wires=range(num_wires))
        return qml.state()

    return circuit
