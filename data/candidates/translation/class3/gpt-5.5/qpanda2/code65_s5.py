# EVAL_META: task_id=65, framework=qpanda2, class=3
from pyqpanda import *
from math import pi
import atexit

machine = CPUQVM()
try:
    machine.set_configure(16, 16)
except Exception:
    try:
        machine.setConfigure(16, 16)
    except Exception:
        pass
machine.init_qvm()
q = machine.qAlloc_many(16)
atexit.register(machine.finalize)

def QFT(n):
    circuit = QCircuit()

    if n > len(q):
        raise ValueError("n exceeds globally allocated qubits")

    def swap_registers(circuit, n):
        for qubit in range(n // 2):
            circuit.insert(SWAP(q[qubit], q[n - qubit - 1]))
        return circuit

    def qft_rotations(circuit, n):
        if n == 0:
            return circuit
        n -= 1
        circuit.insert(H(q[n]))
        for qubit in range(n):
            circuit.insert(CR(q[qubit], q[n], pi / (2 ** (n - qubit))))
        qft_rotations(circuit, n)
        return circuit

    qft_rotations(circuit, n)
    swap_registers(circuit, n)
    return circuit
