# EVAL_META: task_id=9, framework=pennylane, class=3
import pennylane as qml
import numpy as np


def create_efficientSU2():
    num_qubits = 3
    reps = 1
    insert_barriers = True

    dev = qml.device("default.qubit", wires=num_qubits)

    num_params = (reps + 1) * num_qubits * 2

    def rotation_layer(params):
        idx = 0
        for q in range(num_qubits):
            qml.RY(params[idx], wires=q)
            idx += 1
        for q in range(num_qubits):
            qml.RZ(params[idx], wires=q)
            idx += 1

    def entanglement_layer():
        # reversed_linear entanglement
        for i in range(num_qubits - 2, -1, -1):
            qml.CNOT(wires=[i, i + 1])

    @qml.qnode(dev)
    def circuit(params):
        params = np.reshape(params, (reps + 1, num_qubits * 2))
        for r in range(reps):
            rotation_layer(params[r])
            if insert_barriers:
                qml.Barrier(wires=range(num_qubits))
            entanglement_layer()
            if insert_barriers:
                qml.Barrier(wires=range(num_qubits))
        rotation_layer(params[reps])
        return qml.state()

    circuit.num_params = num_params
    return circuit
