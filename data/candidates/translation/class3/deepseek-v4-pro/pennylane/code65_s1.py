# EVAL_META: task_id=65, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def QFT(n):
    def qft_circuit():
        def qft_rotations(wires):
            if len(wires) == 0:
                return
            target = wires[-1]
            rest = wires[:-1]
            qml.Hadamard(target)
            for i, wire in enumerate(rest):
                angle = np.pi / (2 ** (len(rest) - i))
                qml.CPhase(angle, wires=[wire, target])
            qft_rotations(rest)
        wires = list(range(n))
        qft_rotations(wires)
        for i in range(n // 2):
            qml.SWAP(wires=[i, n - i - 1])
    return qft_circuit
