# EVAL_META: task_id=9, framework=pennylane, class=3
import pennylane as qml

def create_efficientSU2():
    class _Parameter(float):
        def __new__(cls, name):
            obj = float.__new__(cls, 0.0)
            obj.name = name
            return obj

        def __repr__(self):
            return self.name

        def __str__(self):
            return self.name

    theta = [_Parameter(f"θ[{i}]") for i in range(12)]

    ops = [
        qml.RY(theta[0], wires=0),
        qml.RY(theta[1], wires=1),
        qml.RY(theta[2], wires=2),
        qml.RZ(theta[3], wires=0),
        qml.RZ(theta[4], wires=1),
        qml.RZ(theta[5], wires=2),
        qml.Barrier(wires=[0, 1, 2]),
        qml.CNOT(wires=[2, 1]),
        qml.CNOT(wires=[1, 0]),
        qml.Barrier(wires=[0, 1, 2]),
        qml.RY(theta[6], wires=0),
        qml.RY(theta[7], wires=1),
        qml.RY(theta[8], wires=2),
        qml.RZ(theta[9], wires=0),
        qml.RZ(theta[10], wires=1),
        qml.RZ(theta[11], wires=2),
    ]

    circuit = qml.tape.QuantumScript(ops)
    circuit.trainable_params = list(range(12))
    return circuit
