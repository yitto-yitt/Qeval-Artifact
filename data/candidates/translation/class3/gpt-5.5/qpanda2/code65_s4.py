# EVAL_META: task_id=65, framework=qpanda2, class=3
from pyqpanda import *
from numpy import pi
import atexit

machine = CPUQVM()
machine.init_qvm()
_MAX_QUBITS = 64
qubits = machine.qAlloc_many(_MAX_QUBITS)

def QFT(n):
    circuit = QCircuit()

    def controlled_phase(control, target, angle):
        if "CP" in globals():
            return CP(control, target, angle)
        if "CR" in globals():
            return CR(control, target, angle)
        sub = QCircuit()
        sub << U1(control, angle / 2)
        sub << CNOT(control, target)
        sub << U1(target, -angle / 2)
        sub << CNOT(control, target)
        sub << U1(target, angle / 2)
        return sub

    def swap_registers(circ, size):
        for qubit in range(size // 2):
            circ << SWAP(qubits[qubit], qubits[size - qubit - 1])
        return circ

    def qft_rotations(circ, size):
        if size == 0:
            return circ
        size -= 1
        circ << H(qubits[size])
        for qubit in range(size):
            circ << controlled_phase(qubits[qubit], qubits[size], pi / (2 ** (size - qubit)))
        qft_rotations(circ, size)
        return circ

    qft_rotations(circuit, n)
    swap_registers(circuit, n)
    return circuit

atexit.register(machine.finalize)
