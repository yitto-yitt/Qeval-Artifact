# EVAL_META: task_id=67, framework=pennylane, class=1
import pennylane as qml
from numpy import pi


def chsh_circuit(alice, bob):
    dev = qml.device('default.qubit', wires=2, shots=None)
    
    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        
        if alice == 0:
            qml.RY(0, wires=0)
        else:
            qml.RY(-pi / 2, wires=0)
            
        if bob == 0:
            qml.RY(-pi / 4, wires=1)
        else:
            qml.RY(pi / 4, wires=1)
            
        return qml.expval(qml.PauliZ(0)), qml.expval(qml.PauliZ(1))
    
    # We need to return a representation of the circuit, 
    # but PennyLane doesn't have a direct circuit object like Qiskit
    # So we create a device and return it after running the circuit
    circuit()
    return dev
