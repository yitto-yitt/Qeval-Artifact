# EVAL_META: task_id=65, framework=pennylane, class=3
import pennylane as qml
from numpy import pi

def QFT(n):
    with qml.tape.QuantumTape() as tape:
        def qft_rotations(n_wires):
            if n_wires == 0:
                return
            n_wires -= 1
            qml.Hadamard(wires=n_wires)
            for qubit in range(n_wires):
                qml.ControlledPhaseShift(pi / 2**(n_wires - qubit), wires=[qubit, n_wires])
            qft_rotations(n_wires)
            
        qft_rotations(n)
        for qubit in range(n // 2):
            qml.SWAP(wires=[qubit, n - qubit - 1])
    return tape
