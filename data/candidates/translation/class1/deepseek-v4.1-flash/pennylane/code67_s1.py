# EVAL_META: task_id=67, framework=pennylane, class=1
import pennylane as qml
import numpy as np

def chsh_circuit(alice, bob):
    dev = qml.device("default.qubit", wires=2, shots=1024)
    
    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        if alice == 0:
            qml.RY(0, wires=0)
        else:
            qml.RY(-np.pi/2, wires=0)
        if bob == 0:
            qml.RY(-np.pi/4, wires=1)
        else:
            qml.RY(np.pi/4, wires=1)
        return qml.sample(wires=[0, 1])
    
    return circuit
