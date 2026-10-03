# EVAL_META: task_id=70, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def create_quantum_circuit_based_h0_cswap012_h1_csdg10():
    with qml.tape.QuantumTape() as circuit:
        qml.Hadamard(wires=0)
        qml.CSWAP(wires=[0, 1, 2])
        qml.Hadamard(wires=1)
        qml.ControlledPhaseShift(-np.pi / 2, wires=[1, 0])
    return circuit
