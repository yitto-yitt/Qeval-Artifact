# EVAL_META: task_id=86, framework=pennylane, class=3
import pennylane as qml

def collect_linear_blocks_with_and_without_limit():
    def circuit_full():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        qml.CNOT(wires=[1, 2])
        qml.CNOT(wires=[2, 3])
        qml.CNOT(wires=[3, 4])
    
    def circuit_limited():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        qml.CNOT(wires=[1, 2])
        qml.CNOT(wires=[2, 3])
        qml.CNOT(wires=[3, 4])
    
    dev = qml.device('default.qubit', wires=5)
    
    # Since PennyLane doesn't have equivalent transpiler passes,
    # we return the same circuit functions for both cases
    return circuit_full, circuit_limited
