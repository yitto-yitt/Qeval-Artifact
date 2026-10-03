# EVAL_META: task_id=145, framework=qpanda, class=3
from pyqpanda import *

def qft_inverse(n):
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(n)
    circuit = QCircuit()
    
    # Implement inverse QFT manually
    for i in range(n//2):
        circuit.insert(SWAP(qubits[i], qubits[n-1-i]))
    
    for i in range(n):
        circuit.insert(H(qubits[i]))
        for j in range(i+1, n):
            angle = -np.pi / (2**(j-i))
            circuit.insert(CR(qubits[j], qubits[i], angle))
    
    return circuit
