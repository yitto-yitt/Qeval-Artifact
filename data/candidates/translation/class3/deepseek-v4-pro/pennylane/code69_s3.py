# EVAL_META: task_id=69, framework=pennylane, class=3
import pennylane as qml
from pennylane import numpy as np

def create_quantum_circuit_based_h0_cs01_h1_csdg10():
    dev = qml.device('default.qubit', wires=2)

    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        qml.ControlledPhaseShift(np.pi / 2, wires=[0, 1])
        qml.Hadamard(wires=1)
        qml.ControlledPhaseShift(-np.pi / 2, wires=[1, 0])
        return qml.state()

    return circuit
