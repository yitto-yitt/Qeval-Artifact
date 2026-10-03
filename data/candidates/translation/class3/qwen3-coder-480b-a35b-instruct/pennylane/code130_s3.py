# EVAL_META: task_id=130, framework=pennylane, class=3
import pennylane as qml

def inv_circuit(n):
    def circuit():
        for i in range(2):
            qml.Hadamard(wires=i+1)

        for i in range(2):
            qml.CNOT(wires=[i+1, i+2+1])
    
    dev = qml.device('default.qubit', wires=n)
    qnode = qml.QNode(circuit, dev)
    adjoint_qnode = qml.adjoint(qnode)
    
    return adjoint_qnode
