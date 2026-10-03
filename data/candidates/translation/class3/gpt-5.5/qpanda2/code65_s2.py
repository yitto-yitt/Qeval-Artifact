# EVAL_META: task_id=65, framework=qpanda2, class=3
from pyqpanda import *
from numpy import pi
import atexit

machine = CPUQVM()
machine.init_qvm()
_qubits = machine.qAlloc_many(64)

def QFT(n):
    circuit = QProg()

    def swap_registers(circuit, n):
        for qubit in range(n // 2):
            circuit.insert(SWAP(_qubits[qubit], _qubits[n - qubit - 1]))
        return circuit

    def qft_rotations(circuit, n):
        if n == 0:
            return circuit
        n -= 1
        circuit.insert(H(_qubits[n]))
        for qubit in range(n):
            circuit.insert(CR(_qubits[qubit], _qubits[n], pi / (2 ** (n - qubit))))
        qft_rotations(circuit, n)
        return circuit

    qft_rotations(circuit, n)
    swap_registers(circuit, n)
    return circuit

atexit.register(machine.finalize)
