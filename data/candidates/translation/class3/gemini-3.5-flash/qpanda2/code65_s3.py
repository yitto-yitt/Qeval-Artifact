# EVAL_META: task_id=65, framework=qpanda2, class=3
import pyqpanda as pq
from numpy import pi

machine = pq.CPUQVM()
machine.init_qvm()
global_qubits = machine.qAlloc_many(100)

def QFT(n):
    circuit = pq.QCircuit()
    qubits = global_qubits[:n]
    
    def swap_registers(circ, n):
        for qubit in range(n // 2):
            circ << pq.SWAP(qubits[qubit], qubits[n - qubit - 1])
            
    def qft_rotations(circ, n):
        if n == 0:
            return
        n -= 1
        circ << pq.H(qubits[n])
        for qubit in range(n):
            circ << pq.CR(qubits[qubit], qubits[n], pi / (2 ** (n - qubit)))
        qft_rotations(circ, n)
        
    qft_rotations(circuit, n)
    swap_registers(circuit, n)
    return circuit

machine.finalize()
