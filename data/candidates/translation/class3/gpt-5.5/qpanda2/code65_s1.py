# EVAL_META: task_id=65, framework=qpanda2, class=3
from pyqpanda import *
from math import pi
import atexit

machine = CPUQVM()
machine.init_qvm()
_MAX_QUBITS = 32
_qubits = machine.qAlloc_many(_MAX_QUBITS)
atexit.register(machine.finalize)

def QFT(n):
    if n < 0 or n > _MAX_QUBITS:
        raise ValueError("n must be between 0 and _MAX_QUBITS")

    circuit = QCircuit()

    def swap_registers(circuit, n):
        for qubit in range(n // 2):
            circuit << SWAP(_qubits[qubit], _qubits[n - qubit - 1])
        return circuit

    def qft_rotations(circuit, n):
        if n == 0:
            return circuit
        n -= 1
        circuit << H(_qubits[n])
        for qubit in range(n):
            if "CP" in globals():
                circuit << CP(_qubits[qubit], _qubits[n], pi / (2 ** (n - qubit)))
            else:
                circuit << CR(_qubits[qubit], _qubits[n], pi / (2 ** (n - qubit)))
        return qft_rotations(circuit, n)

    qft_rotations(circuit, n)
    swap_registers(circuit, n)
    return circuit
