# EVAL_META: task_id=66, framework=pennylane, class=2
import pennylane as qml
from numpy import arccos, sqrt


def w_state():
    dev = qml.device('default.qubit', wires=3, shots=1000)
    
    @qml.qnode(dev)
    def circuit():
        qml.RY(2 * arccos(1 / sqrt(3)), wires=0)
        qml.CH(wires=[0, 1])
        qml.CNOT(wires=[1, 2])
        qml.CNOT(wires=[0, 1])
        qml.X(wires=0)
        
        # Measure all qubits
        return [qml.sample(qml.PauliZ(i)) for i in range(3)]
    
    result = circuit()
    return result
