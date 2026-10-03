# EVAL_META: task_id=9, framework=pennylane, class=3
import pennylane as qml

def create_efficientSU2():
    num_qubits = 3
    reps = 1
    dev = qml.device("default.qubit", wires=num_qubits)

    @qml.qnode(dev)
    def circuit(params):
        param_idx = 0
        for r in range(reps + 1):
            for q in range(num_qubits):
                qml.RY(params[param_idx], wires=q)
                param_idx += 1
                qml.RZ(params[param_idx], wires=q)
                param_idx += 1
            if r < reps:
                qml.Barrier(wires=range(num_qubits))
                for q in range(num_qubits - 1, 0, -1):
                    qml.CNOT(wires=[q, q - 1])
        return qml.state()

    return circuit
