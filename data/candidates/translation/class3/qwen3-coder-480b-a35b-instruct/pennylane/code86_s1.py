# EVAL_META: task_id=86, framework=pennylane, class=3
import pennylane as qml

def collect_linear_blocks_with_and_without_limit():
    # Create a 5-qubit device
    dev = qml.device('default.qubit', wires=5)
    
    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        qml.CNOT(wires=[1, 2])
        qml.CNOT(wires=[2, 3])
        qml.CNOT(wires=[3, 4])
        return qml.state()
    
    # In PennyLane, there isn't a direct equivalent to Qiskit's CollectLinearFunctions
    # We return the circuit function itself as the closest equivalent representation
    # Since PennyLane doesn't have the same transpilation passes as Qiskit,
    # we return the same circuit for both cases
    return circuit, circuit
