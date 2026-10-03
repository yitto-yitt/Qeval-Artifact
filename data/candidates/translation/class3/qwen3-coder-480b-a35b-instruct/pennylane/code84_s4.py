# EVAL_META: task_id=84, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def controlled_custom_unitary_circuit():
    def custom_unitary(params, wires):
        qml.Rot(*params, wires=wires)
    
    dev = qml.device('default.qubit', wires=2)
    
    @qml.qnode(dev)
    def circuit():
        # Define the custom unitary parameters
        params = [0.3, 0.2, 0.1]
        
        # Apply the controlled custom unitary
        qml.ctrl(custom_unitary, control=0)(params, wires=1)
        
        return qml.state()
    
    # We need to return a representation of the circuit
    # Since PennyLane doesn't have the same circuit object as Qiskit,
    # we'll create a template that can be used
    class ControlledCustomUnitaryTemplate:
        def __init__(self):
            self.params = [0.3, 0.2, 0.1]
            self.wires = [0, 1]
        
        def expand(self):
            dev = qml.device('default.qubit', wires=2)
            
            @qml.qnode(dev)
            def template():
                qml.ctrl(qml.Rot, control=0)(*(self.params), wires=1)
                return qml.state()
            
            return template
    
    template_instance = ControlledCustomUnitaryTemplate()
    return template_instance
