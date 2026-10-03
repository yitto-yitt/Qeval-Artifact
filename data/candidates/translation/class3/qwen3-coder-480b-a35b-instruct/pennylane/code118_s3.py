# EVAL_META: task_id=118, framework=pennylane, class=3
import pennylane as qml

def create_c3sx_circuit():
    def circuit():
        # Implementing C3SX gate using controlled operations
        # C3SX is equivalent to applying X gate controlled by 3 qubits
        qml.ctrl(qml.PauliX, control=[0, 1, 2])(wires=3)
    
    dev = qml.device('default.qubit', wires=4)
    qnode = qml.QNode(circuit, dev)
    return qnode
