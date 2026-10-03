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
    
    # In PennyLane, we just return the circuit functions as there's no direct equivalent
    # to Qiskit's transpiler passes for collecting linear functions
    return circuit_full, circuit_limited
