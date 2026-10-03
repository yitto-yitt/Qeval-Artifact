# EVAL_META: task_id=10, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def create_operator():
    U = np.array([[0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0]])
    tape = qml.tape.QuantumScript([qml.QubitUnitary(U, wires=[0, 1])])
    compiled_tape = qml.compile(tape, basis_set=["CNOT", "RX", "RY", "RZ"])
    return compiled_tape
