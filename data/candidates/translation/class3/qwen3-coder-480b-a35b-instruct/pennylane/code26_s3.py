# EVAL_META: task_id=26, framework=pennylane, class=3
import pennylane as qml


def bell_dag():
    dev = qml.device('default.qubit', wires=3)
    
    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.expval(qml.PauliZ(0))
    
    tape = circuit.qtape
    return tape
