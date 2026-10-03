# EVAL_META: task_id=65, framework=qpanda2, class=3
import pyqpanda as pq
from numpy import pi

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(100)

def QFT(n):
    circuit = pq.QCircuit()
    
    def qft_rotations(circuit, n):
        if n == 0:
            return
        n -= 1
        circuit << pq.H(qubits[n])
        for qubit in range(n):
            angle = pi / (2 ** (n - qubit))
            circuit << pq.U1(qubits[n], angle).control([qubits[qubit]])
        qft_rotations(circuit, n)
        
    def swap_registers(circuit, n):
        for qubit in range(n // 2):
            circuit << pq.SWAP(qubits[qubit], qubits[n - qubit - 1])
            
    qft_rotations(circuit, n)
    swap_registers(circuit, n)
    return circuit

machine.finalize()
