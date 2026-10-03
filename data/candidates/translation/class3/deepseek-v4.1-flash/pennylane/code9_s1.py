# EVAL_META: task_id=9, framework=pennylane, class=3
import pennylane as qml

def create_efficientSU2():
    dev = qml.device("default.qubit", wires=3)
    
    @qml.qnode(dev)
    def circuit(params):
        for q in range(3):
            qml.RY(params[2*q], wires=q)
            qml.RZ(params[2*q+1], wires=q)
        qml.Barrier(wires=range(3))
        for q in range(2):
            qml.CNOT(wires=[q, q+1])
        qml.Barrier(wires=range(3))
        for q in range(3):
            qml.RY(params[6 + 2*q], wires=q)
            qml.RZ(params[6 + 2*q+1], wires=q)
        qml.Barrier(wires=range(3))
        return qml.state()
    
    return circuit
