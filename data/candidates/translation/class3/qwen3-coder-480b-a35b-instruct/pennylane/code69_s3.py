# EVAL_META: task_id=69, framework=pennylane, class=3
import pennylane as qml

def create_quantum_circuit_based_h0_cs01_h1_csdg10():
    def circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        qml.S(wires=1)
        qml.adjoint(qml.CNOT)(wires=[0, 1])
        qml.Hadamard(wires=1)
        qml.adjoint(qml.CNOT)(wires=[1, 0])
        qml.adjoint(qml.S)(wires=0)
        qml.CNOT(wires=[1, 0])
    return circuit
