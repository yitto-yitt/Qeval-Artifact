# EVAL_META: task_id=9, framework=pennylane, class=3
import pennylane as qml

def create_efficientSU2():
    with qml.tape.QuantumTape() as tape:
        for i in range(3):
            qml.RY(0.0, wires=i)
            qml.RZ(0.0, wires=i)
        qml.Barrier(wires=[0, 1, 2])
        
        qml.CNOT(wires=[0, 1])
        qml.CNOT(wires=[1, 2])
        qml.Barrier(wires=[0, 1, 2])
        
        for i in range(3):
            qml.RY(0.0, wires=i)
            qml.RZ(0.0, wires=i)
        qml.Barrier(wires=[0, 1, 2])
        
    return tape
