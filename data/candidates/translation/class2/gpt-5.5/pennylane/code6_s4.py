# EVAL_META: task_id=6, framework=pennylane, class=2
import pennylane as qml


def create_state_prep(num_qubits):
    dev = qml.device("default.qubit", wires=num_qubits)

    @qml.qnode(dev)
    def circuit():
        basis_state = [0] * num_qubits
        basis_state[-1] = 1
        qml.BasisState(basis_state, wires=range(num_qubits))
        return qml.state()

    return circuit
