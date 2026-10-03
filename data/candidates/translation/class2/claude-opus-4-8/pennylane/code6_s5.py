# EVAL_META: task_id=6, framework=pennylane, class=2
import pennylane as qml


def create_state_prep(num_qubits):
    def circuit():
        state = [0.0] * (2 ** num_qubits)
        state[1] = 1.0
        qml.StatePrep(state, wires=range(num_qubits))
        return qml.state()
    return circuit
