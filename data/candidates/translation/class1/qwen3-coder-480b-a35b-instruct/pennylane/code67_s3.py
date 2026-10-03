# EVAL_META: task_id=67, framework=pennylane, class=1
import pennylane as qml
from numpy import pi


def chsh_circuit(alice, bob):
    dev = qml.device('default.qubit', wires=2, shots=1)
    
    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        
        qml.Barrier(wires=[0, 1])
        
        if alice == 0:
            qml.RY(0, wires=0)
        else:
            qml.RY(-pi / 2, wires=0)
        
        if bob == 0:
            qml.RY(-pi / 4, wires=1)
        else:
            qml.RY(pi / 4, wires=1)
        
        return qml.sample()
    
    # Run the circuit to initialize it
    circuit()
    
    # Create a new device with the same operations but without sampling for returning the operations
    ops = []
    wires = 2
    
    # Initialize the operations list based on the circuit logic
    ops.append(qml.Hadamard(wires=0))
    ops.append(qml.CNOT(wires=[0, 1]))
    ops.append(qml.Barrier(wires=[0, 1]))
    
    if alice == 0:
        ops.append(qml.RY(0, wires=0))
    else:
        ops.append(qml.RY(-pi / 2, wires=0))
    
    if bob == 0:
        ops.append(qml.RY(-pi / 4, wires=1))
    else:
        ops.append(qml.RY(pi / 4, wires=1))
    
    # Since PennyLane doesn't have a direct circuit object like Qiskit,
    # we return a function that creates the circuit when called
    def execute_circuit():
        dev_local = qml.device('default.qubit', wires=2, shots=1)
        
        @qml.qnode(dev_local)
        def inner_circuit():
            for op in ops:
                qml.apply(op)
            return qml.sample()
        
        return inner_circuit()
    
    return execute_circuit
