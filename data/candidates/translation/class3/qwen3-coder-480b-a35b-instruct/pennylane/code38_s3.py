# EVAL_META: task_id=38, framework=pennylane, class=3
import pennylane as qml

def create_quantum_circuit_based_h0_crz01_h1_cry10(theta):
    def circuit():
        qml.Hadamard(wires=0)
        qml.CRX(theta, wires=[0, 1])
        qml.Hadamard(wires=1)
        qml.CRY(theta, wires=[1, 0])
    return circuit
