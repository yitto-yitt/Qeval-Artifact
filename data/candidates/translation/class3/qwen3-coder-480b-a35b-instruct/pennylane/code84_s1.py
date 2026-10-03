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
        
        # Apply controlled custom unitary: control on wire 0, target on wire 1
        qml.ctrl(custom_unitary, control=0)(params, wires=1)
        
        return qml.state()
    
    # We need to return a representation of the circuit operations
    # Since we can't return the qnode directly as a circuit object,
    # we create a template that represents the operation
    class ControlledCustomUnitaryTemplate:
        def __init__(self):
            self.params = [0.3, 0.2, 0.1]
            self.wires = [0, 1]
            
        def __call__(self, params=None):
            if params is None:
                params = self.params
            # Execute the operation
            dev = qml.device('default.qubit', wires=2)
            
            @qml.qnode(dev)
            def exec_circuit():
                qml.ctrl(qml.Rot, control=0)(*params, wires=1)
                return qml.state()
            
            return exec_circuit()
    
    return ControlledCustomUnitaryTemplate()
