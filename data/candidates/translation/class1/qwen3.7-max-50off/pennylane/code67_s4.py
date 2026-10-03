# EVAL_META: task_id=67, framework=pennylane, class=1
import pennylane as qml
from numpy import pi

def chsh_circuit(alice, bob):
    with qml.tape.QuantumTape() as tape:
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        
        if alice == 0:
            qml.RY(0, wires=0)
        else:
            qml.RY(-pi / 2, wires=0)
            
        qml.measure(0)
        
        if bob == 0:
            qml.RY(-pi / 4, wires=1)
        else:
            qml.RY(pi / 4, wires=1)
            
        qml.measure(1)
        
    return tape
