# EVAL_META: task_id=61, framework=pennylane, class=1
import pennylane as qml


def create_quantum_circuit_with_one_qubit_and_measure():
    device = qml.device("default.qubit", wires=["q"], shots=1)

    @qml.qnode(device)
    def circuit():
        return qml.sample(wires=["q"])

    circuit()
    return circuit
