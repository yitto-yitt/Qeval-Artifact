# EVAL_META: task_id=69, framework=pennylane, class=3
import pennylane as qml


def create_quantum_circuit_based_h0_cs01_h1_csdg10():
    with qml.tape.QuantumTape() as tape:
        qml.Hadamard(wires=0)
        qml.ctrl(qml.S(wires=1), control=0)
        qml.Hadamard(wires=1)
        qml.ctrl(qml.adjoint(qml.S(wires=0)), control=1)
    return tape
