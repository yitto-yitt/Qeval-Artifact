# EVAL_META: task_id=9, framework=pennylane, class=3
import pennylane as qml

def create_efficientSU2():
    with qml.queuing.AnnotatedQueue() as q:
        for i in range(3):
            qml.RY(0.0, wires=i)
            qml.RZ(0.0, wires=i)
        qml.Barrier(wires=[0, 1, 2])
        
        qml.CNOT(wires=[2, 1])
        qml.CNOT(wires=[1, 0])
        qml.Barrier(wires=[0, 1, 2])
        
        for i in range(3):
            qml.RY(0.0, wires=i)
            qml.RZ(0.0, wires=i)
        qml.Barrier(wires=[0, 1, 2])
        
    return qml.tape.QuantumScript.from_queue(q)
