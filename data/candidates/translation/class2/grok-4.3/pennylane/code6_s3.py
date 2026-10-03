# EVAL_META: task_id=6, framework=pennylane, class=2
import pennylane as qml

def create_state_prep(num_qubits):
    def circuit():
        state = [0] * num_qubits
        if num_qubits > 0:
            state[-1] = 1
        qml.BasisState(state, wires=range(num_qubits))
    return circuit
