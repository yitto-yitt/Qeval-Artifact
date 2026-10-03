# EVAL_META: task_id=65, framework=qpanda2, class=3
from pyqpanda import CPUQVM, QCircuit, H, CR, SWAP
from numpy import pi

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(64)


def QFT(n):
    circuit = QCircuit()

    def qft_rotations(circuit, m):
        if m == 0:
            return circuit
        m -= 1
        circuit << H(qubits[m])
        for qubit in range(m):
            circuit << CR(qubits[qubit], qubits[m], pi / 2 ** (m - qubit))
        qft_rotations(circuit, m)
        return circuit

    def swap_registers(circuit, m):
        for qubit in range(m // 2):
            circuit << SWAP(qubits[qubit], qubits[m - qubit - 1])
        return circuit

    qft_rotations(circuit, n)
    swap_registers(circuit, n)
    return circuit


machine.finalize()
