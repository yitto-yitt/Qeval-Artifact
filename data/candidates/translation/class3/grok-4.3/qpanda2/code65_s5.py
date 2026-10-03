# EVAL_META: task_id=65, framework=qpanda2, class=3
import pyqpanda as pq
from numpy import pi

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(20)

def QFT(n):
    circuit = pq.QCircuit()
    def swap_registers(circuit, n):
        for qubit in range(n//2):
            circuit << pq.SWAP(qubits[qubit], qubits[n-qubit-1])
        return circuit
    def qft_rotations(circuit, n):
        if n == 0:
            return circuit
        n -= 1
        circuit << pq.H(qubits[n])
        for qubit in range(n):
            circuit << pq.CPHASE(qubits[qubit], qubits[n], pi/2**(n-qubit))
        qft_rotations(circuit, n)
    
    qft_rotations(circuit, n)
    swap_registers(circuit, n)
    return circuit

machine.finalize()
