# EVAL_META: task_id=65, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def QFT(n):
    def qft_rotations(active_n):
        if active_n == 0:
            return
        target = active_n - 1
        qml.Hadamard(wires=target)
        for qubit in range(target):
            angle = np.pi / (2 ** (target - qubit))
            qml.ControlledPhaseShift(angle, wires=[qubit, target])
        qft_rotations(target)
    
    qft_rotations(n)
    for qubit in range(n // 2):
        qml.SWAP(wires=[qubit, n - qubit - 1])
