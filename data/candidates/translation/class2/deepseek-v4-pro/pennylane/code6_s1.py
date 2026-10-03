# EVAL_META: task_id=6, framework=pennylane, class=2
import pennylane as qml

def create_state_prep(num_qubits):
    dev = qml.device("default.qubit", wires=num_qubits)
    @qml.qnode(dev)
    def circuit():
        # |00...01> = last qubit in |1>, all others in |0>
        qml.BasisState([0] * (num_qubits - 1) + [1], wires=range(num_qubits))
        return qml.state()
    return circuit
