# EVAL_META: task_id=84, framework=pennylane, class=3
import pennylane as qml

def controlled_custom_unitary_circuit():
    with qml.tape.QuantumTape() as circuit:
        qml.ctrl(qml.U3, control=0)(0.3, 0.2, 0.1, wires=1)
    return circuit
