# EVAL_META: task_id=71, framework=pennylane, class=3
import pennylane as qml

def create_quantum_circuit_based_h0_csx01_h1():
    def circuit():
        qml.Hadamard(wires=0)
        qml.ISWAP(wires=[0, 1])
        qml.RZ(-qml.numpy.pi/2, wires=0)
        qml.RZ(-qml.numpy.pi/2, wires=1)
        qml.Hadamard(wires=0)
        qml.Hadamard(wires=1)
        qml.ISWAP(wires=[0, 1])
        qml.RZ(qml.numpy.pi/2, wires=0)
        qml.RZ(qml.numpy.pi/2, wires=1)
        qml.Hadamard(wires=0)
        qml.Hadamard(wires=1)
        qml.Hadamard(wires=1)
    
    return circuit
