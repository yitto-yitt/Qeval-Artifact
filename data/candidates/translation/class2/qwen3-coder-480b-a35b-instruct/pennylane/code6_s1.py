# EVAL_META: task_id=6, framework=pennylane, class=2
import pennylane as qml


def create_state_prep(num_qubits):
    dev = qml.device('default.qubit', wires=num_qubits)
    
    @qml.qnode(dev)
    def circuit():
        qml.PauliX(wires=0)
        return qml.state()
    
    return circuit()
