# EVAL_META: task_id=9, framework=pennylane, class=3
import pennylane as qml

def create_efficientSU2():
    def circuit(params):
        qml.StronglyEntanglingLayers(weights=params, wires=range(3), imprimitive=qml.CNOT)
    
    # Create the template structure similar to EfficientSU2
    # EfficientSU2 is equivalent to StronglyEntanglingLayers in PennyLane
    num_layers = 1
    params_shape = qml.StronglyEntanglingLayers.shape(n_layers=num_layers, n_wires=3)
    params = qml.numpy.random.uniform(size=params_shape)
    
    dev = qml.device('default.qubit', wires=3)
    
    @qml.qnode(dev)
    def ansatz(params):
        qml.StronglyEntanglingLayers(weights=params, wires=range(3), imprimitive=qml.CNOT)
        return qml.state()
    
    return lambda: ansatz(params)
