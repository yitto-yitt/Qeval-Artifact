# EVAL_META: task_id=118, framework=pennylane, class=3
import pennylane as qml

def create_c3sx_circuit():
    def circuit():
        # Implement C3SX gate using controlled operations
        # C3SX is a 4-qubit gate where 3 control qubits apply SX (sqrt(X)) to target
        qml.ctrl(qml.SX, control=[0, 1, 2])(wires=3)
    
    dev = qml.device('default.qubit', wires=4)
    qnode = qml.QNode(circuit, dev)
    qnode()
    return qnode
