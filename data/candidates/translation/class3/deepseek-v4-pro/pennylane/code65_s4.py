# EVAL_META: task_id=65, framework=pennylane, class=3
import pennylane as qml
from numpy import pi

def QFT(n):
    ops = []
    def qft_rotations(m):
        if m == 0:
            return
        m -= 1
        ops.append(qml.Hadamard(wires=m))
        for qubit in range(m):
            ops.append(qml.ControlledPhaseShift(pi/2**(m-qubit), wires=[qubit, m]))
        qft_rotations(m)
    def swap_registers():
        for qubit in range(n//2):
            ops.append(qml.SWAP(wires=[qubit, n-qubit-1]))
    qft_rotations(n)
    swap_registers()
    return qml.tape.QuantumScript(ops)
