# EVAL_META: task_id=9, framework=pennylane, class=3
import pennylane as qml

def create_efficientSU2():
    with qml.tape.QuantumTape() as tape:
        qml.RY(0.0, wires=0)
        qml.RZ(0.0, wires=0)
        qml.RY(0.0, wires=1)
        qml.RZ(0.0, wires=1)
        qml.RY(0.0, wires=2)
        qml.RZ(0.0, wires=2)
        
        qml.Barrier(wires=[0, 1, 2])
        
        qml.CNOT(wires=[0, 1])
        qml.CNOT(wires=[1, 2])
        
        qml.Barrier(wires=[0, 1, 2])
        
        qml.RY(0.0, wires=0)
        qml.RZ(0.0, wires=0)
        qml.RY(0.0, wires=1)
        qml.RZ(0.0, wires=1)
        qml.RY(0.0, wires=2)
        qml.RZ(0.0, wires=2)
        
    return tape
