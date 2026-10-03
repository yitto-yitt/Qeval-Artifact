# EVAL_META: task_id=145, framework=qpanda2, class=3
import pyqpanda as pq
import math

# Global QVM initialization
machine = pq.CPUQVM()
machine.init_qvm()
global_qubits = machine.qAlloc_many(24)

def qft_inverse(n):
    qubits = global_qubits[:n]
    circuit = pq.QCircuit()
    for i in range(n):
        circuit << pq.H(qubits[i])
        for j in range(i + 1, n):
            theta = 2 * math.pi / (2 ** (j - i + 1))
            circuit << pq.CPHASE(qubits[j], qubits[i], theta)
    for i in range(n // 2):
        circuit << pq.SWAP(qubits[i], qubits[n - i - 1])
    return circuit.dagger()

machine.finalize()
