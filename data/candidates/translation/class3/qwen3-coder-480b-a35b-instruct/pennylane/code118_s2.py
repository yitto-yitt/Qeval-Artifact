# EVAL_META: task_id=118, framework=pennylane, class=3
import pennylane as qml

def create_c3sx_circuit():
    def circuit():
        # Implement C3SX gate using Toffoli gates and single-qubit rotations
        # C3SX can be decomposed as controlled-controlled-controlled-X
        qml.Toffoli(wires=[0, 1, 2])
        qml.S(wires=2)
        qml.Toffoli(wires=[0, 1, 2])
        qml.adjoint(qml.S)(wires=2)
        
        # Additional decomposition for the fourth qubit (square root X part)
        # The C3SX gate is a controlled-controlled-controlled-SX gate
        # We need to implement it as a multi-controlled RX gate with angle pi/2
        qml.ctrl(qml.RX, control=[0, 1, 2])(numpy.pi / 2, wires=3)
    
    dev = qml.device('default.qubit', wires=4)
    qnode = qml.QNode(circuit, dev)
    return qnode

# Actually implement the C3SX properly using multi-controlled operations
import pennylane as qml
import numpy

def create_c3sx_circuit():
    def circuit():
        # A C3SX gate is a three-controlled square root X gate
        # This means when all three control qubits (0,1,2) are 1, apply SX to target (3)
        # SX gate is sqrt(X) = RZ(-pi/2)RY(pi/2)RZ(pi/2) *or* RX(pi/2) up to global phase
        
        # Using the multi-controlled RX gate with angle pi/2 (which is SX)
        qml.ctrl(qml.RX, control=[0, 1, 2])(numpy.pi / 2, wires=3)
    
    dev = qml.device('default.qubit', wires=4)
    qnode = qml.QNode(circuit, dev)
    return qnode
