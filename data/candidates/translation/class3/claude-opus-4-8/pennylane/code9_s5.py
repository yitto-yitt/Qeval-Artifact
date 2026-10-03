# EVAL_META: task_id=9, framework=pennylane, class=3
import pennylane as qml


def create_efficientSU2():
    num_qubits = 3
    reps = 1
    num_params = (reps + 1) * num_qubits * 2

    dev = qml.device("default.qubit", wires=num_qubits)

    @qml.qnode(dev)
    def circuit(params):
        idx = 0
        for _ in range(reps):
            for q in range(num_qubits):
                qml.RY(params[idx], wires=q)
                idx += 1
            for q in range(num_qubits):
                qml.RZ(params[idx], wires=q)
                idx += 1
            for i in reversed(range(num_qubits - 1)):
                qml.CNOT(wires=[i, i + 1])
        for q in range(num_qubits):
            qml.RY(params[idx], wires=q)
            idx += 1
        for q in range(num_qubits):
            qml.RZ(params[idx], wires=q)
            idx += 1
        return qml.state()

    circuit.num_params = num_params
    return circuit
