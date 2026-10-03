# EVAL_META: task_id=52, framework=pennylane, class=1
import pennylane as qml

def send_bits(bitstring):
    with qml.tape.QuantumTape() as tape:
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        
        if bitstring[1] == "1":
            qml.PauliZ(wires=0)
        if bitstring[0] == "1":
            qml.PauliX(wires=0)
            
        qml.CNOT(wires=[0, 1])
        qml.Hadamard(wires=0)
        
        qml.sample(wires=0)
        qml.sample(wires=1)
        
    return tape
