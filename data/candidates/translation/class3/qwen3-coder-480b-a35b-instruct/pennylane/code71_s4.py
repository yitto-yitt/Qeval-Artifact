# EVAL_META: task_id=71, framework=pennylane, class=3
import pennylane as qml

def create_quantum_circuit_based_h0_csx01_h1():
    def circuit():
        qml.Hadamard(wires=0)
        qml.ctrl(qml.SX, control=0)(wires=1)
        qml.Hadamard(wires=1)
    return circuit
