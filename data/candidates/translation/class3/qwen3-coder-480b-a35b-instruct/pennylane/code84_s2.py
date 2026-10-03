# EVAL_META: task_id=84, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def controlled_custom_unitary_circuit():
    def custom_unitary(params, wires):
        qml.Rot(params[0], params[1], params[2], wires=wires)
    
    dev = qml.device('default.qubit', wires=2)
    
    @qml.qnode(dev)
    def circuit():
        # Apply controlled version of the custom unitary
        qml.ctrl(custom_unitary, control=0)([0.3, 0.2, 0.1], wires=1)
        return qml.state()
    
    # We need to return the operation that would be applied, not execute the circuit
    # Create a template for the controlled custom unitary
    def controlled_custom_template(params, control_wire, target_wire):
        qml.ctrl(qml.Rot, control=control_wire)(params[0], params[1], params[2], wires=target_wire)
    
    # Since we can't return a circuit directly like in Qiskit, 
    # we create a device and qnode that implements the desired operation
    dev = qml.device('default.qubit', wires=2)
    
    @qml.qnode(dev)
    def build_circuit():
        qml.ctrl(qml.Rot, control=0)(0.3, 0.2, 0.1, wires=1)
        return qml.state()
    
    return build_circuit
