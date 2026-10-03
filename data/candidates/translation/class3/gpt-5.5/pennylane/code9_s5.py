# EVAL_META: task_id=9, framework=pennylane, class=3
import pennylane as qml

def create_efficientSU2():
    params = [f"θ[{i}]" for i in range(12)]

    ops = [
        qml.RY(params[0], wires=0),
        qml.RY(params[1], wires=1),
        qml.RY(params[2], wires=2),
        qml.RZ(params[3], wires=0),
        qml.RZ(params[4], wires=1),
        qml.RZ(params[5], wires=2),
        qml.Barrier(wires=[0, 1, 2]),
        qml.CNOT(wires=[2, 1]),
        qml.CNOT(wires=[1, 0]),
        qml.Barrier(wires=[0, 1, 2]),
        qml.RY(params[6], wires=0),
        qml.RY(params[7], wires=1),
        qml.RY(params[8], wires=2),
        qml.RZ(params[9], wires=0),
        qml.RZ(params[10], wires=1),
        qml.RZ(params[11], wires=2),
    ]

    return qml.tape.QuantumScript(ops=ops, measurements=[])
