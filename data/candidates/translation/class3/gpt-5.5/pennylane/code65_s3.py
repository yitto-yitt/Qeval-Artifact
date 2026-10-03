# EVAL_META: task_id=65, framework=pennylane, class=3
import pennylane as qml
from numpy import pi

def QFT(n):
    ops = []

    def swap_registers(n):
        for qubit in range(n // 2):
            ops.append(qml.SWAP(wires=[qubit, n - qubit - 1]))

    def qft_rotations(n):
        if n == 0:
            return
        n -= 1
        ops.append(qml.Hadamard(wires=n))
        for qubit in range(n):
            ops.append(qml.ControlledPhaseShift(pi / 2 ** (n - qubit), wires=[qubit, n]))
        qft_rotations(n)

    qft_rotations(n)
    swap_registers(n)
    return qml.tape.QuantumScript(ops=ops)
