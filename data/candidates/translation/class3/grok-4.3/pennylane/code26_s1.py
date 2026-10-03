# EVAL_META: task_id=26, framework=pennylane, class=3
import pennylane as qml

def bell_dag():
    with qml.tape.QuantumTape() as tape:
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        qml.sample(wires=[0])
    return tape
