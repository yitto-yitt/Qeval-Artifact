# EVAL_META: task_id=65, framework=qpanda, class=3
from pyqpanda3.core import *
import numpy as np

_machines = []

def QFT(n):
    machine = init_quantum_machine(QMachineType.CPU)
    _machines.append(machine)
    qubits = machine.qAllocMany(n)
    
    circuit = QCircuit()
    
    def swap_registers(circuit, n):
        for qubit in range(n // 2):
            circuit << SWAP(qubits[qubit], qubits[n - qubit - 1])
        return circuit

    def qft_rotations(circuit, n):
        if n == 0:
            return circuit
        n -= 1
        circuit << H(qubits[n])
        for qubit in range(n):
            circuit << CR(qubits[qubit], qubits[n], np.pi / 2**(n - qubit))
        qft_rotations(circuit, n)
        
    qft_rotations(circuit, n)
    swap_registers(circuit, n)
    return circuit
