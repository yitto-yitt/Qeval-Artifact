# EVAL_META: task_id=65, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QCircuit, H, SWAP, CPHASE
import numpy as np

def QFT(n):
    machine = CPUQVM()
    machine.init_qvm()
    qubits = machine.q_alloc_many(n)
    
    circuit = QCircuit()
    
    def qft_rotations(circuit, qubits, n):
        if n == 0:
            return
        n -= 1
        circuit << H(qubits[n])
        for qubit in range(n):
            circuit << CPHASE(qubits[qubit], qubits[n], np.pi / (2 ** (n - qubit)))
        qft_rotations(circuit, qubits, n)
        
    def swap_registers(circuit, qubits, n):
        for qubit in range(n // 2):
            circuit << SWAP(qubits[qubit], qubits[n - qubit - 1])
            
    qft_rotations(circuit, qubits, n)
    swap_registers(circuit, qubits, n)
    
    # Keep machine alive by attaching it to the circuit object
    circuit.machine = machine
    return circuit
