# EVAL_META: task_id=65, framework=pennylane, class=3
import pennylane as qml
from numpy import pi

def QFT(n):
    dev = qml.device("default.qubit", wires=n)

    @qml.qnode(dev)
    def circuit():
        def swap_registers(n_qubits):
            for qubit in range(n_qubits // 2):
                qml.SWAP(wires=[qubit, n_qubits - qubit - 1])

        def qft_rotations(n_qubits):
            if n_qubits == 0:
                return
            n_local = n_qubits - 1
            qml.Hadamard(wires=n_local)
            for qubit in range(n_local):
                qml.ControlledPhaseShift(pi / 2 ** (n_local - qubit), wires=[qubit, n_local])
            qft_rotations(n_local)

        qft_rotations(n)
        swap_registers(n)
        return qml.state()

    return circuit
