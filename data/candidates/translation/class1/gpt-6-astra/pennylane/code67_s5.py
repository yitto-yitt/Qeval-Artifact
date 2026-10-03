# EVAL_META: task_id=67, framework=pennylane, class=1
from numpy import pi
import pennylane as qml


def chsh_circuit(alice, bob):
    device = qml.device("default.qubit", wires=2)

    @qml.set_shots(shots=1)
    @qml.qnode(device)
    def circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        qml.Barrier(wires=[0, 1])
        qml.RY(0 if alice == 0 else -pi / 2, wires=0)
        alice_result = qml.measure(0)
        qml.RY(-pi / 4 if bob == 0 else pi / 4, wires=1)
        return qml.sample(alice_result), qml.sample(wires=1)

    circuit()
    return circuit
