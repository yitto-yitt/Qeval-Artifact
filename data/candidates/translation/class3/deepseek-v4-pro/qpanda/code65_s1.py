# EVAL_META: task_id=65, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit, CP, Swap, H, pi

def QFT(n):
    circuit = QuantumCircuit(n)
    def swap_registers(circuit, n):
        for qubit in range(n // 2):
            circuit << Swap(circuit[qubit], circuit[n - qubit - 1])
        return circuit
    def qft_rotations(circuit, n):
        if n == 0:
            return circuit
        n -= 1
        circuit << H(circuit[n])
        for qubit in range(n):
            circuit << CP(circuit[qubit], circuit[n], pi / 2**(n - qubit))
        qft_rotations(circuit, n)
    qft_rotations(circuit, n)
    swap_registers(circuit, n)
    return circuit
